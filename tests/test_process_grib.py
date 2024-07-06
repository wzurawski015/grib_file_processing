#!/usr/bin/env python
# Ścieżka: tests/test_process_grib.py

import unittest
from grib_processing.process_grib import parse_filename

class TestProcessGrib(unittest.TestCase):
    def test_parse_filename(self):
        filename = "fc20240701_00+003gl"
        result = parse_filename(filename)
        expected = "2024-07-01 00:15"
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
