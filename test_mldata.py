#!/usr/bin/env python
import unittest

from mldata import *

class TestDataParser(unittest.TestCase):

    def setUp(self):
        self.exset = parse_c45('example')

    def test_parsed(self):
        self.assertTrue(self.exset is not None)

    def test_schema(self):
        self.assertEqual(len(self.exset.schema), 6)
        correct_types = (Feature.Type.ID,
                         Feature.Type.BINARY,
                         Feature.Type.NOMINAL,
                         Feature.Type.CONTINUOUS,
                         Feature.Type.NOMINAL,
                         Feature.Type.CLASS)
        for feature, correct_type in zip(self.exset.schema, correct_types):
            self.assertEqual(feature.type, correct_type)

    def test_data(self):
        self.assertEqual(len(self.exset), 10)

    def test_missing(self):
        self.assertTrue(self.exset[7][4] is None)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestDataParser))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
