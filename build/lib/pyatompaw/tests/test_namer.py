
import unittest

import os
from os.path import dirname

from ..namer import *


class TestNamer(unittest.TestCase):

    def setUp(self):
        self.namer = AtompawNamer('6-C/carbon')

    def test_rootname(self):
        """Test that a basename is always provided"""
        directory = 'NoBasename'
        self.namer.rootname = directory
        self.assertEqual(self.namer.dirname, directory)
        self.assertNotEqual(self.namer.rootname, directory)
        self.assertTrue(self.namer.basename)

    def test_filenames(self):
        """Check that file names are contained in the main directory"""
        self.assertEqual(self.namer.dirname, dirname(self.namer.inputname))
        self.assertEqual(self.namer.dirname, dirname(self.namer.wfn_pdf))
        self.assertEqual(self.namer.dirname, dirname(self.namer.logderiv_pdf))
        self.assertEqual(self.namer.dirname, dirname(self.namer.wfn(1)))
        self.assertEqual(self.namer.dirname, dirname(self.namer.logderiv(1)))
        self.assertEqual(self.namer.dirname, dirname(self.namer.tprod(1)))


if __name__ == '__main__':
    unittest.main()

