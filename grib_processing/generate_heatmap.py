#!/usr/bin/env python
# Ścieżka: grib_processing/generate_heatmap.py

import os
import matplotlib.pyplot as plt
import numpy as np
import yaml

# Wczytaj konfigurację
with open('/app/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def generate_heatmap(file_datetime, type_of_level, level, lats, lons, values, units):
    """Generuje mapę ciepła."""
    plt.figure(figsize=(10, 6))
    plt.scatter(lons, lats, c=values, cmap='coolwarm', s=10, edgecolor='none')
    plt.colorbar(label=f"Temperature ({units})")
    plt.title(f"{file_datetime}, {type_of_level}, {level}")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')

    filename = f"{file_datetime.replace(' ', '_').replace(':', '')}_{type_of_level}_{level}.png"
    output_path = os.path.join(config['paths']['image_folder'], filename)
    plt.savefig(output_path)
    plt.close()
