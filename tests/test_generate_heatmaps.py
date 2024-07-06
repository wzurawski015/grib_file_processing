# tests/test_generate_heatmaps.py

import unittest
import numpy as np
from grib_processing.generate_heatmap import generate_heatmap

class TestGenerateHeatmaps(unittest.TestCase):

    def test_generate_heatmap(self):
        data = {
            'latitudes': np.array([0, 1, 2]),
            'longitudes': np.array([0, 1, 2]),
            'values': np.array([1, 2, 3])
        }
        output_path = 'test_heatmap.png'
        title = 'Test Heatmap'
        generate_heatmap(data, output_path, title)
        # Sprawdzenie, czy plik został zapisany
        self.assertTrue(os.path.exists(output_path))
        # Usunięcie pliku po teście
        os.remove(output_path)

if __name__ == '__main__':
    unittest.main()
