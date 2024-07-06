#!/usr/bin/env python
# Ścieżka: grib_processing/move_files.py

import os
import yaml
import shutil

# Wczytaj plik konfiguracyjny
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Ścieżki katalogów
source_dir = config['source_directory']
target_dir = config['target_directory']

def move_files():
    """Przenoszenie plików z katalogu źródłowego do katalogu docelowego."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for filename in os.listdir(source_dir):
        if '_1_surface_0.png' in filename:
            shutil.move(os.path.join(source_dir, filename), os.path.join(target_dir, filename))
    print("Pliki zostały pomyślnie przeniesione")

if __name__ == '__main__':
    move_files()
