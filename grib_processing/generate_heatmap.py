#!/usr/bin/env python
# Ścieżka: grib_processing/generate_heatmap.py

import matplotlib.pyplot as plt
import numpy as np

def generate_heatmap(data, output_path, title):
    """Funkcja do generowania mapy ciepła"""
    latitudes = np.array(data['latitudes'])
    longitudes = np.array(data['longitudes'])
    values = np.array(data['values'])

    plt.figure(figsize=(10, 8))
    plt.imshow(values.reshape(len(latitudes), len(longitudes)), cmap='coolwarm', interpolation='nearest')
    plt.colorbar(label='Temperature (K)')
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(output_path)
    plt.close()
