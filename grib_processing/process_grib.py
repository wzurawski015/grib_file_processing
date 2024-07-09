import matplotlib
matplotlib.use('Agg')  # Ustawienie backendu na tryb nieinteraktywny

import re
import os
import yaml
import pygrib
import logging
import numpy as np
from generate_heatmap import generate_heatmap

# Konfiguracja logowania
log_file = 'process_grib.log'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler(log_file),
                        logging.StreamHandler()
                    ])
logger = logging.getLogger('process_grib')

# Ścieżka do pliku konfiguracyjnego
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))

# Wczytaj plik konfiguracyjny
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Ścieżki katalogów
data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['data_directory_grib']))
flask_data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['data_directory_flask']))
logger.debug(f'Configured data directory: {data_directory}')
logger.debug(f'Configured Flask data directory: {flask_data_directory}')

def parse_filename(filename):
    """
    Funkcja do parsowania nazwy pliku GRIB.

    Args:
        filename (str): Nazwa pliku GRIB.

    Returns:
        tuple: Zawierający datę i godzinę, typ pliku oraz inne parametry.
    """
    try:
        pattern = r'fc(\d{4})(\d{2})(\d{2})_(\d{2})\+(\d{3})gl'
        match = re.match(pattern, filename)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            hour = match.group(4)
            intervals = int(match.group(5))

            base_time = f"{year}-{month}-{day} {hour}:00"
            minutes = intervals * 5
            additional_hours = minutes // 60
            additional_minutes = minutes % 60

            final_hour = int(hour) + additional_hours
            final_minute = additional_minutes

            if final_minute >= 60:
                final_hour += 1
                final_minute -= 60
            if final_hour >= 24:
                final_hour -= 24
                day = int(day) + 1
                day = f"{day:02d}"

            final_time = f"{year}-{month}-{day} {final_hour:02d}:{final_minute:02d}"
            return (final_time, 'gl', f"{intervals:03d}")
        else:
            raise ValueError("Nazwa pliku nie pasuje do wzorca")
    except Exception as e:
        logger.error(f"Błąd podczas parsowania nazwy pliku {filename}: {e}")
        raise

def process_grib_files(data_directory, flask_data_directory):
    """
    Funkcja do przetwarzania plików GRIB w danym katalogu.

    Args:
        data_directory (str): Ścieżka do katalogu z plikami GRIB.
        flask_data_directory (str): Ścieżka do katalogu, gdzie zapisywane będą mapy ciepła.
    """
    try:
        logger.info(f"Analizowanie danych z katalogu: {data_directory}")
        if not os.path.exists(data_directory):
            logger.error(f"Katalog {data_directory} nie istnieje.")
            return

        if not os.path.exists(flask_data_directory):
            os.makedirs(flask_data_directory)
            logger.debug(f"Stworzono katalog {flask_data_directory}.")

        logger.debug(f"Rozpoczynam przetwarzanie plików w katalogu: {data_directory}")

        files_processed = 0
        for filename in os.listdir(data_directory):
            if not filename.startswith('.'):
                filepath = os.path.join(data_directory, filename)
                logger.debug(f"Przetwarzanie pliku: {filepath}")
                try:
                    grbs = pygrib.open(filepath)
                    for i, grb in enumerate(grbs):
                        parameter_name = grb.parameterName
                        if parameter_name != 'T Temperature K':
                            logger.debug(f'Pomijanie rekordu {i+1} z pliku {filename} z powodu parametru: {parameter_name}')
                            continue
                        
                        lat, lon = grb.latlons()
                        data = grb.values

                        # Logowanie kształtu tablic
                        logger.debug(f"Kształt lat: {lat.shape}, Kształt lon: {lon.shape}, Kształt data: {data.shape}")
                        
                        if lat.shape != lon.shape or lat.shape != data.shape:
                            logger.error(f"Liczba wartości ({data.size}) nie pasuje do liczby latitudes ({lat.size}) i longitudes ({lon.size})")
                            continue

                        # Logowanie wszystkich dostępnych kluczy i wartości rekordu GRIB
                        logger.debug(f"Klucze i wartości rekordu GRIB (plik: {filename}, rekord: {i+1}):")
                        for key in grb.keys():
                            try:
                                logger.debug(f"{key}: {grb[key]}")
                            except KeyError as ke:
                                logger.warning(f"Nie znaleziono klucza {key} (plik: {filename}, rekord: {i+1}): {ke}")
                            except Exception as e:
                                logger.error(f"Błąd podczas odczytu klucza {key} (plik: {filename}, rekord: {i+1}): {e}")

                        # Generowanie mapy ciepła
                        latitudes = lat.flatten()
                        longitudes = lon.flatten()
                        values = data.flatten()
                        
                        level = grb.level
                        param = grb.typeOfLevel

                        final_time, file_type, intervals = parse_filename(filename)
                        output_filename = f"{final_time.replace(' ', '_').replace(':', '')}_{i+1}_{param}_{level}.png"
                        output_path = os.path.join(flask_data_directory, output_filename)
                        logger.debug(f'Output path for heatmap: {output_path}')
                        title = f'Mapa ciepła {final_time} {param} {level}'

                        # Debugowanie danych przekazywanych do generate_heatmap
                        logger.debug(f'Latitudes: {latitudes[:5]}, Longitudes: {longitudes[:5]}, Values: {values[:5]}')

                        generate_heatmap(latitudes, longitudes, values, output_path, title)
                        logger.info(f'Mapa ciepła została zapisana jako {output_path}')
                    
                    grbs.close()
                    files_processed += 1
                except Exception as e:
                    logger.error(f"Błąd podczas przetwarzania pliku {filepath} (plik: {filename}): {e}")
                    raise

        if files_processed == 0:
            logger.info("Nie znaleziono żadnych plików GRIB do przetworzenia.")
        else:
            logger.info(f"Przetworzono {files_processed} plików GRIB.")
    except FileNotFoundError as fnf_error:
        logger.error(f"Katalog {data_directory} nie istnieje: {fnf_error}")
        raise
    except Exception as e:
        logger.error(f"Niespodziewany błąd podczas przetwarzania katalogu {data_directory}: {e}")
        raise

if __name__ == '__main__':
    try:
        process_grib_files(data_directory, flask_data_directory)
    except Exception as e:
        logger.critical(f"Niepowodzenie podczas przetwarzania plików GRIB: {e}")
