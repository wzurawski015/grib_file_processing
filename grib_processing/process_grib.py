#!/usr/bin/env python
# Ścieżka: grib_processing/process_grib.py

import os
import logging
from datetime import datetime, timedelta
import yaml
from eccodes import *

# Wczytaj konfigurację
with open('/app/config.yaml', 'r') as f:
    config = yaml.safe_load(f)

logging.basicConfig(level=logging.DEBUG, format='%(message)s')

def parse_filename(filename):
    """Parsuje nazwę pliku, aby wyodrębnić datę i godzinę."""
    try:
        base, time_part = filename.split('_')
        date_part = base[2:10]
        hour_part = time_part[:2]
        interval_part = time_part[3:6]

        year = int(date_part[:4])
        month = int(date_part[:6])
        day = int(date_part[6:8])
        hour = int(hour_part)
        interval = int(interval_part)

        total_minutes = hour * 60 + interval * 5
        file_datetime = datetime(year, month, day) + timedelta(minutes=total_minutes)

        return file_datetime.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        logging.error(f"Error parsing filename {filename}: {e}")
        return "Invalid datetime"

def process_grib_file(filepath):
    """Przetwarza pojedynczy plik GRIB."""
    with open(filepath, 'rb') as ifile:
        while True:
            igrib = codes_grib_new_from_file(ifile)
            if igrib is None:
                break

            try:
                units = codes_get(igrib, 'units')
                if units == "K":
                    type_of_level = codes_get(igrib, 'typeOfLevel')
                    level = codes_get(igrib, 'level')
                    lats = codes_get_array(igrib, 'latitudes')
                    lons = codes_get_array(igrib, 'longitudes')
                    values = codes_get_values(igrib)
                    file_datetime = parse_filename(os.path.basename(filepath))

                    # Generuj mapę ciepła dla każdego rekordu
                    generate_heatmap(file_datetime, type_of_level, level, lats, lons, values, units)
            except Exception as e:
                logging.error(f"Error processing GRIB message: {e}")
            finally:
                codes_release(igrib)

def process_grib_files(directory):
    """Przetwarza wszystkie pliki GRIB w określonym katalogu."""
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        for file in files:
            process_grib_file(os.path.join(directory, file))
    except Exception as e:
        logging.error(f"Error processing files in directory {directory}: {e}")

if __name__ == "__main__":
    process_grib_files(config['paths']['data'])
