import unittest
import sys
import os

# Dodanie katalogu głównego do PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grib_processing.process_grib import parse_filename

class TestProcessGrib(unittest.TestCase):

    def test_parse_filename(self):
        """
        Testuje funkcję parse_filename
        """
        filename = 'fc20240628_18+024gl'
        result = parse_filename(filename)
        expected = ('2024-06-28 20:00', 'gl', '024')
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
