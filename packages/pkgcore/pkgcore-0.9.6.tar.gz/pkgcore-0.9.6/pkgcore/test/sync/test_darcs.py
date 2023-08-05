# Copyright: 2006 Brian Harring <ferringb@gmail.com>
# License: GPL2/BSD

from pkgcore.sync import base, darcs
from pkgcore.test.sync import make_bogus_syncer, make_valid_syncer
from snakeoil.test import TestCase

bogus = make_bogus_syncer(darcs.darcs_syncer)
valid = make_valid_syncer(darcs.darcs_syncer)


class TestDarcsSyncer(TestCase):

    def test_uri_parse(self):
        self.assertEqual(darcs.darcs_syncer.parse_uri("darcs+http://dar"),
            "http://dar")
        self.assertRaises(base.uri_exception, darcs.darcs_syncer.parse_uri,
            "darcs://dar")
        self.assertRaises(base.syncer_exception, bogus,
            "/tmp/foon", "darcs+http://foon.com/dar")
        o = valid("/tmp/foon", "darcs+http://dar")
        self.assertEqual(o.uri, "http://dar")
