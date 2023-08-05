import os

from snakeoil.demandload import demandload

from pkgcheck import base

demandload(
    'pkgcore.log:logger',
    'pkgcore.pkgsets.glsa:GlsaDirSet',
    'pkgcore.restrictions:packages,values',
    'pkgcore.restrictions.util:collect_package_restrictions',
    'snakeoil.osutils:abspath,pjoin',
    'snakeoil.strings:pluralism',
)


class VulnerablePackage(base.Error):
    """Packages marked as vulnerable by GLSAs."""

    __slots__ = ("category", "package", "version", "arches", "glsa")
    threshold = base.versioned_feed

    def __init__(self, pkg, glsa):
        super(VulnerablePackage, self).__init__()
        self._store_cpv(pkg)
        arches = set()
        for v in collect_package_restrictions(glsa, ["keywords"]):
            if isinstance(v.restriction, values.ContainmentMatch):
                arches.update(x.lstrip("~") for x in v.restriction.vals)
            else:
                raise Exception("unexpected restriction sequence- %s in %s" %
                                (v.restriction, glsa))
        keys = set(x.lstrip("~") for x in pkg.keywords if not x.startswith("-"))
        if arches:
            self.arches = tuple(sorted(arches.intersection(keys)))
            assert self.arches
        else:
            self.arches = tuple(sorted(keys))
        self.glsa = str(glsa)

    @property
    def short_desc(self):
        return "vulnerable via %s, keyword%s: %s" % (
            self.glsa, pluralism(self.arches), ', '.join(self.arches))


class TreeVulnerabilitiesReport(base.Template):
    """Scan for vulnerable ebuilds in the tree.

    Requires a GLSA directory for vulnerability info.
    """

    feed_type = base.versioned_feed
    known_results = (VulnerablePackage,)

    @staticmethod
    def mangle_argparser(parser):
        parser.plugin.add_argument(
            "--glsa-dir", dest='glsa_location',
            help="source directory for glsas; tries to autodetermine it, may "
                 "be required if no glsa dirs are known")

    @staticmethod
    def check_args(parser, namespace):
        namespace.glsa_enabled = True
        glsa_loc = namespace.glsa_location
        if glsa_loc is not None:
            if not os.path.isdir(glsa_loc):
                parser.error(
                    "--glsa-dir '%r' doesn't exist" % glsa_loc)
        else:
            if not namespace.repo_bases:
                parser.error('a target repo or overlayed repo must be specified')
            for repo_base in namespace.repo_bases:
                candidate = pjoin(repo_base, "metadata", "glsa")
                if os.path.isdir(candidate):
                    if glsa_loc is None:
                        glsa_loc = candidate
                    else:
                        parser.error(
                            'multiple glsa sources is unsupported (detected '
                            '%s and %s). Pick one with --glsa-dir.' % (
                                glsa_loc, candidate))
            if glsa_loc is None:
                # form of 'optional' limiting; if they are using -c, force the
                # error, else disable
                if namespace.selected_checks is not None:
                    parser.error(
                        "--glsa-dir must be specified, couldn't find glsa source")
                namespace.glsa_enabled = False
                if namespace.verbose:
                    logger.warn(
                        "disabling GLSA checks due to no glsa source "
                        "being found, and the check not being explicitly enabled; "
                        "this behaviour may change")
                return

        namespace.glsa_location = abspath(glsa_loc)

    def __init__(self, options):
        super(TreeVulnerabilitiesReport, self).__init__(options)
        self.glsa_dir = options.glsa_location
        self.enabled = False
        self.vulns = {}

    def start(self):
        if not self.options.glsa_enabled:
            return
        # this is a bit brittle
        for r in GlsaDirSet(self.glsa_dir):
            if len(r) > 2:
                self.vulns.setdefault(
                    r[0].key, []).append(packages.AndRestriction(*r[1:]))
            else:
                self.vulns.setdefault(r[0].key, []).append(r[1])

    def finish(self, reporter):
        self.vulns.clear()

    def feed(self, pkg, reporter):
        if not self.options.glsa_enabled:
            return
        for vuln in self.vulns.get(pkg.key, []):
            if vuln.match(pkg):
                reporter.add_report(VulnerablePackage(pkg, vuln))
