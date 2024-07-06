import unittest
import numpy as np
import os
import sys
import matplotlib

# Dodanie katalogu głównego do PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

matplotlib.use('Agg')  # Ustawienie bezgłowego backendu
from grib_processing.generate_heatmap import generate_heatmap

class TestGenerateHeatmaps(unittest.TestCase):

    def test_generate_heatmap(self):
        """
        Testuje funkcję generate_heatmap
        """
        latitudes = np.array([50.0, 51.0, 52.0])
        longitudes = np.array([19.0, 20.0, 21.0])
        values = np.array([10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0])
        output_path = 'test_output.png'
        title = 'Test Heatmap'
        generate_heatmap(latitudes, longitudes, values, output_path, title)

        # Sprawdzenie, czy plik został zapisany
        self.assertTrue(os.path.isfile(output_path))

        # Opcjonalnie: usunięcie pliku po teście
        if os.path.isfile(output_path):
            os.remove(output_path)

if __name__ == '__main__':
    unittest.main()
