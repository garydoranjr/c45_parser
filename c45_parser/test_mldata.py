#!/usr/bin/env python
import unittest

from mldata import *

class TestMLData(unittest.TestCase):

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

    def test_selection(self):
        subset = ExampleSet(ex for ex in self.exset if ex[2] == 'Monday')
        self.assertEqual(len(subset), 2)
        self.assertEqual(subset.schema, self.exset.schema)

    def test_empty_set(self):
        empty = ExampleSet()
        self.assertTrue(empty.schema is None)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMLData))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite())
