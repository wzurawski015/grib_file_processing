# tests/test_process_grib.py

import unittest
from grib_processing.process_grib import parse_filename

class TestProcessGrib(unittest.TestCase):

    def test_parse_filename(self):
        filename = "fc20240628_18+024gl"
        expected = ("2024-06-28 20:00", 'gl')
        result = parse_filename(filename)
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
