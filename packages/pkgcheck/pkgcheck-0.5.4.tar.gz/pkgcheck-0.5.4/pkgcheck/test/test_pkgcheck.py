from pkgcore.test.scripts import helpers
from snakeoil.test import TestCase

from pkgcheck.scripts import pkgcheck


class CommandlineTest(TestCase, helpers.ArgParseMixin):

    _argparser = pkgcheck.scan

    def test_parser(self):
        self.assertError(
            'no target repo specified and '
            'current directory is not inside a known repo')
        self.assertError(
            "argument -r/--repo: couldn't find repo 'spork'",
            '-r', 'spork')
