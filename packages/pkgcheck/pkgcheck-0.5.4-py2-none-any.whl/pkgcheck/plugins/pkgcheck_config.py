"""Extra default config sections from pkgcheck."""

from pkgcore.config import basics

from pkgcheck import base

pkgcore_plugins = {
    'global_config': [{
        'repo': basics.ConfigSectionFromStringDict({
            'class': 'pkgcheck.base.Scope',
            'scopes': str(base.repository_scope),
            }),
        'no-arch': basics.ConfigSectionFromStringDict({
            'class': 'pkgcheck.base.Blacklist',
            'patterns': 'unstable_only stale_unstable imlate',
            }),
        'all': basics.ConfigSectionFromStringDict({
            'class': 'pkgcheck.base.Blacklist',
            'patterns': '',
            }),
        }],
    }
