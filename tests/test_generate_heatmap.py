#!/usr/bin/env python
# Ścieżka: tests/test_generate_heatmap.py

import unittest
import os
import numpy as np
from grib_processing.generate_heatmap import generate_heatmap

class TestGenerateHeatmap(unittest.TestCase):
    def test_generate_heatmap(self):
        data = np.random.rand(10, 10)
        output_file = "test_heatmap.png"
        title = "Test Heatmap"
        generate_heatmap(data, output_file, title)
        self.assertTrue(os.path.exists(output_file))
        os.remove(output_file)

if __name__ == '__main__':
    unittest.main()
