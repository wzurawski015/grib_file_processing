import re
import os
import yaml
import pygrib
import logging

# Konfiguracja logowania
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('process_grib')

# Ścieżka do pliku konfiguracyjnego
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))

# Wczytaj plik konfiguracyjny
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Ścieżki katalogów
data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['data_directory_grib']))
logger.debug(f'Configured data directory: {data_directory}')

def parse_filename(filename):
    """
    Funkcja do parsowania nazwy pliku GRIB.

    Args:
        filename (str): Nazwa pliku GRIB.

    Returns:
        tuple: Zawierający datę i godzinę, typ pliku oraz inne parametry.
    """
    try:
        # Wzorzec do dopasowania nazwy pliku GRIB
        pattern = r'fc(\d{4})(\d{2})(\d{2})_(\d{2})\+(\d{3})gl'
        match = re.match(pattern, filename)
        if match:
            year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            hour = match.group(4)
            intervals = int(match.group(5))

            # Obliczanie czasu końcowego na podstawie interwałów
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

def process_grib_files(data_directory):
    """
    Funkcja do przetwarzania plików GRIB w danym katalogu.

    Args:
        data_directory (str): Ścieżka do katalogu z plikami GRIB.
    """
    try:
        if not os.path.exists(data_directory):
            logger.error(f"Katalog {data_directory} nie istnieje.")
            return

        logger.debug(f"Rozpoczynam przetwarzanie plików w katalogu: {data_directory}")

        files_processed = 0
        for filename in os.listdir(data_directory):
            # Ignorowanie plików i katalogów ukrytych
            if not filename.startswith('.'):
                filepath = os.path.join(data_directory, filename)
                logger.debug(f"Przetwarzanie pliku: {filepath}")
                try:
                    # Otwieranie pliku GRIB za pomocą pygrib
                    grbs = pygrib.open(filepath)
                    for grb in grbs:
                        # Przykład przetwarzania wiadomości z pliku GRIB
                        logger.debug(grb)
                    grbs.close()
                    files_processed += 1
                except Exception as e:
                    logger.error(f"Błąd podczas przetwarzania pliku {filepath}: {e}")
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

# Przykład użycia
if __name__ == '__main__':
    try:
        process_grib_files(data_directory)
    except Exception as e:
        logger.critical(f"Niepowodzenie podczas przetwarzania plików GRIB: {e}")
