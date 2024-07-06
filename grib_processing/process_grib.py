# grib_processing/process_grib.py

import re
import os
import pygrib

def parse_filename(filename):
    """
    Funkcja do parsowania nazwy pliku GRIB.
    
    Args:
        filename (str): Nazwa pliku GRIB.
        
    Returns:
        tuple: Zawierający datę i godzinę, typ pliku oraz inne parametry.
    """
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
        
        # Konwersja do pełnej godziny i minut
        final_hour = int(hour) + additional_hours
        final_minute = additional_minutes
        
        final_time = f"{year}-{month}-{day} {final_hour:02d}:{final_minute:02d}"
        return (final_time, 'gl')
    else:
        raise ValueError("Nazwa pliku nie pasuje do wzorca")

def process_grib_files(data_directory):
    # Przykład funkcji przetwarzającej pliki GRIB
    for filename in os.listdir(data_directory):
        if filename.endswith('.grb'):
            filepath = os.path.join(data_directory, filename)
            # Otwieranie pliku GRIB za pomocą pygrib
            grbs = pygrib.open(filepath)
            for grb in grbs:
                # Przykład przetwarzania wiadomości z pliku GRIB
                print(grb)
            grbs.close()
