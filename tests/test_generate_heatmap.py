#!/usr/bin/env python
# Ścieżka: tests/test_generate_heatmap.py

import unittest
import numpy as np
from grib_processing.generate_heatmap import generate_heatmap

class TestGenerateHeatmap(unittest.TestCase):
    def test_generate_heatmap(self):
        lats = np.random.uniform(low=-90, high=90, size=100)
        lons = np.random.uniform(low=-180, high=180, size=100)
        values = np.random.uniform(low=240, high=310, size=100)
        try:
            generate_heatmap("2024-07-05 12:00", "surface", 0, lats, lons, values, "K")
        except Exception as e:
            self.fail(f"generate_heatmap raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
