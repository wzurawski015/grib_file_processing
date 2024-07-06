#!/usr/bin/env python
# Ścieżka: grib_processing/generate_heatmap.py

import matplotlib.pyplot as plt
import numpy as np

def generate_heatmap(latitudes, longitudes, values, output_path, title):
    """
    Funkcja do generowania mapy ciepła.

    Args:
        latitudes (list): Lista szerokości geograficznych.
        longitudes (list): Lista długości geograficznych.
        values (list): Lista wartości (np. temperatury) do wizualizacji.
        output_path (str): Ścieżka do zapisu wygenerowanej mapy ciepła.
        title (str): Tytuł mapy ciepła.

    """
    plt.figure(figsize=(10, 8))
    plt.imshow(values, cmap='coolwarm', interpolation='nearest', extent=(min(longitudes), max(longitudes), min(latitudes), max(latitudes)))
    plt.colorbar(label='Temperature (K)')
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(output_path)
    plt.close()
