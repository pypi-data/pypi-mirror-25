|pypi| |test| |coverage|

========
pkgcheck
========

Dependencies
============

pkgcheck is developed alongside pkgcore_. To run the development version of
pkgcheck you will need the development version of pkgcore.

The metadata.xml checks require lxml to be installed.

Installing
==========

No installation is strictly required, just run the ``pkgcheck`` script and
things should work. For a more permanent install see the following options:

Installing latest pypi release in a virtualenv::

    pip install pkgcheck

Installing from git in a virtualenv (latest snakeoil/pkgcore are often required)::

    pip install https://github.com/pkgcore/snakeoil/archive/master.tar.gz
    pip install https://github.com/pkgcore/pkgcore/archive/master.tar.gz
    pip install https://github.com/pkgcore/pkgcheck/archive/master.tar.gz

Installing from a tarball or git repo::

    python setup.py install
    pplugincache pkgcheck.plugins

Tests
=====

A standalone test runner is integrated in setup.py; to run, just execute::

    python setup.py test

In addition, a tox config is provided so the testsuite can be run in a
virtualenv setup against all supported python versions. To run tests for all
environments just execute **tox** in the root directory of a repo or unpacked
tarball. Otherwise, for a specific python version execute something similar to
the following::

    tox -e py27

Notes
=====

Currently full tree scans will use a large amount of memory (up to ~1.7GB) in
part due to pkgcore's restriction design in relation to the expanding use of
transitive use flag dependencies across the tree. To alleviate this
pkgcore.restrictions_ will be refactored, probably leading to splitting
conditionals off into their own set.

Configuration
=============

No configuration is required, but some configuration makes ``pkgcheck``
easier to use.

Suites
------

With no configuration it will try to guess the repository to use based
on your working directory and the list of repositories pkgcore knows
about. This will usually not quite work because the same location
often has multiple "repositories" with a slightly different
configuration and ``pkgcheck`` cannot guess which one to use.

Defining "suites" in the configuration solves this ambiguity. A
"suite" contains a target repository, optionally a source repository
to use as a base and optionally a set of checks to run. If there is a
single suite with a target repository containing the current directory
it is used. So with the following suite definition in
``~/.config/pkgcore/pkgcore.conf``::

  [pkgcheck-gentoo-suite]
  class=pkgcheck.base.Suite
  target_repo=gentoo

you can run ``pkgcheck scan`` with no further arguments inside your portage
directory and it will do the right thing.

Make sure the target repo properly specifies its masters in
metadata/layout.conf if it's meant to be an overlay, otherwise many errors are
likely to be produced relating to missing licenses, categories, dependencies,
etc.

Finally, you can define a different checkset per suite::

  [pkgcheck-gentoo-suite]
  class=pkgcheck.base.Suite
  target_repo=gentoo
  checkset=no-arch-checks

This disables checks that are not interesting unless you can set
stable keywords for this suite. See Checksets_ for more information.

Instead of relying on the working directory to pick the right suite
you can specify one explicitly with ``pkgcheck scan -s/--suite``.

Checksets
---------

By default ``pkgcheck scan`` runs all available checks. This is not always
desired. For example, checks about missing stable keywords are often
just noise in the output for ebuild devs. A checkset defines a subset
of checks to run. There are two kinds: one enabling a specific set of
checks and one running every available check except for the specified
ones. Examples::

  [no-arch-checks]
  class=pkgcheck.base.Blacklist
  patterns=unstable_only stale_unstable imlate

  [only-arch-checks]
  class=pkgcheck.base.Whitelist
  patterns=unstable_only stale_unstable imlate

The first disables the three specified checks, the second enables only
those three. For available names see ``pkgcheck show --checks``.

``patterns`` is a whitespace-separated list. If the values are strings
they need to match a component of the name in ``pkgcheck show --checks``
exactly. If it looks like a regexp (currently defined as "contains a +
or \*") this needs to match the entire name.

Checksets called ``no-arch-checks`` and ``all-checks`` are defined by
default.

There are various ways to pick the checkset to use: ``pquery
--checkset``, the checkset setting of a suite and setting
``default=true`` on a checkset in the configuration.

Reporters
---------

By default the output is in a colorful human-readable format. For full
tree checks this format may not be optimal since it is a bit hard to
grep. To use an output format that prints everything on one line, put
this in your configuration::

  [pkgcheck-plain-reporter]
  class=pkgcheck.reporters.plain_reporter
  default=true

To use a non-default reporter use ``pkgcheck scan -R/--reporter``. To see the
reporters available use ``pconfig configurables
pkgcheck_reporter_factory``.


.. _`Installing python modules`: http://docs.python.org/inst/
.. _pkgcore: https://github.com/pkgcore/pkgcore
.. _pkgcore.restrictions: https://github.com/pkgcore/pkgcore/issues/80

.. |pypi| image:: https://img.shields.io/pypi/v/pkgcheck.svg
    :target: https://pypi.python.org/pypi/pkgcheck
.. |test| image:: https://travis-ci.org/pkgcore/pkgcheck.svg?branch=master
    :target: https://travis-ci.org/pkgcore/pkgcheck
.. |coverage| image:: https://codecov.io/gh/pkgcore/pkgcheck/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/pkgcore/pkgcheck
