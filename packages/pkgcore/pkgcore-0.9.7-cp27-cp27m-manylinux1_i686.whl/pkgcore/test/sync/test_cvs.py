# Copyright: 2006 Brian Harring <ferringb@gmail.com>
# License: GPL2/BSD

from pkgcore.sync import base, cvs
from pkgcore.test.sync import make_bogus_syncer, make_valid_syncer
from snakeoil.test import TestCase

bogus = make_bogus_syncer(cvs.cvs_syncer)
valid = make_valid_syncer(cvs.cvs_syncer)


class TestCVSSyncer(TestCase):

    def test_uri_parse(self):
        self.assertRaises(
            base.syncer_exception, bogus,
            "/tmp/foon", "cvs+hopefully_nonexistent_binary://foon.com/dar")
        o = valid("/tmp/foon", "cvs://dar:module")
        self.assertEqual(o.uri, ":anoncvs:dar")
        self.assertEqual(o.module, "module")
        self.assertEqual(o.rsh, None)
        self.assertEqual(o.env["CVSROOT"], ":anoncvs:dar")

        o = valid("/tmp/foon", "cvs+pserver://dar:module")
        self.assertEqual(o.uri, ":pserver:dar")
        self.assertEqual(o.module, "module")
        self.assertEqual(o.rsh, None)
        self.assertEqual(o.env["CVSROOT"], ":pserver:dar")

        o = valid("/tmp/foon", "cvs+/bin/sh://dar:module")
        self.assertEqual(o.rsh, "/bin/sh")
        self.assertEqual(o.uri, ":ext:dar")
        self.assertEqual(o.env["CVSROOT"], ":ext:dar")
        self.assertEqual(o.env["CVS_RSH"], "/bin/sh")
