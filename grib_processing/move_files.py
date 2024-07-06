#!/usr/bin/env python
# Ścieżka: grib_processing/move_files.py

import os
import shutil
import yaml

# Wczytaj konfigurację
with open('/app/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

def move_files():
    """Przenosi pliki zawierające w nazwie _1_surface_0.png do odpowiedniego katalogu."""
    src_dir = config['paths']['image_folder']
    dest_dir = os.path.join(config['paths']['image_folder'], '1_surface_0')
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    for file in os.listdir(src_dir):
        if '_1_surface_0.png' in file:
            shutil.move(os.path.join(src_dir, file), os.path.join(dest_dir, file))

if __name__ == "__main__":
    move_files()
