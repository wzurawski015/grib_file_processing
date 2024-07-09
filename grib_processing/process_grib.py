import matplotlib
matplotlib.use('Agg')  # Ustawienie backendu na tryb nieinteraktywny

import re
import os
import yaml
import pygrib
import logging
import numpy as np
from typing import Tuple, List
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

# Ścieżki katalogów i inne ustawienia z config.yaml
data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['data_directory_grib']))
flask_data_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['data_directory_flask']))
display_specific_points = config['display_specific_points']
specific_latitudes = config['specific_latitudes']
specific_longitudes = config['specific_longitudes']

logger.debug(f'Configured data directory: {data_directory}')
logger.debug(f'Configured Flask data directory: {flask_data_directory}')
logger.debug(f'Configured display specific points: {display_specific_points}')
logger.debug(f'Configured specific latitudes: {specific_latitudes}')
logger.debug(f'Configured specific longitudes: {specific_longitudes}')

def parse_filename(filename: str) -> Tuple[str, str, str]:
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
        year, month, day, hour, intervals = match.groups()
        intervals = int(intervals)

        base_time = f"{year}-{month}-{day} {hour}:00"
        minutes = intervals * 5
        additional_hours, additional_minutes = divmod(minutes, 60)

        final_hour = int(hour) + additional_hours
        final_minute = additional_minutes

        if final_minute >= 60:
            final_hour += 1
            final_minute -= 60
        if final_hour >= 24:
            final_hour -= 24
            day = f"{int(day) + 1:02d}"

        final_time = f"{year}-{month}-{day} {final_hour:02d}:{final_minute:02d}"
        return final_time, 'gl', f"{intervals:03d}"
    else:
        raise ValueError(f"Nazwa pliku {filename} nie pasuje do wzorca")

def find_global_min_max(data_directory: str) -> Tuple[float, float]:
    """
    Funkcja do znalezienia globalnej minimalnej i maksymalnej wartości temperatury
    w skali Celsjusza dla wszystkich plików GRIB.

    Args:
        data_directory (str): Ścieżka do katalogu z plikami GRIB.

    Returns:
        tuple: Globalna minimalna i maksymalna wartość temperatury.
    """
    global_min = float('inf')
    global_max = float('-inf')
    
    for filename in os.listdir(data_directory):
        if filename.startswith('.'):
            continue

        filepath = os.path.join(data_directory, filename)
        logger.debug(f"Analizowanie pliku: {filepath}")
        try:
            with pygrib.open(filepath) as grbs:
                for grb in grbs:
                    if grb.parameterName == 'T Temperature K' and grb.level == 2:
                        data = grb.values - 273.15  # Konwersja z Kelwinów na Celsjusze
                        global_min = min(global_min, np.min(data))
                        global_max = max(global_max, np.max(data))
        except Exception as e:
            logger.error(f"Błąd podczas analizy pliku {filepath}: {e}")
            raise
    
    logger.debug(f"Globalna minimalna wartość temperatury: {global_min}")
    logger.debug(f"Globalna maksymalna wartość temperatury: {global_max}")
    return global_min, global_max

def log_grib_keys(grb):
    """
    Funkcja do logowania nazw i wartości kluczy w rekordach GRIB.

    Args:
        grb: Obiekt GRIB.
    """
    keys = [
        'globalDomain', 'GRIBEditionNumber', 'eps', 'offsetSection0', 'section0Length', 'totalLength', 'editionNumber',
        'WMO', 'productionStatusOfProcessedData', 'section1Length', 'wrongPadding', 'table2Version', 'centre',
        'centreDescription', 'generatingProcessIdentifier', 'gridDefinition', 'indicatorOfParameter', 'parameterName',
        'parameterUnits', 'indicatorOfTypeOfLevel', 'pressureUnits', 'typeOfLevelECMF', 'typeOfLevel', 'level', 
        'yearOfCentury', 'month', 'day', 'hour', 'minute', 'second', 'unitOfTimeRange', 'P1', 'P2', 'timeRangeIndicator',
        'numberIncludedInAverage', 'numberMissingFromAveragesOrAccumulations', 'centuryOfReferenceTimeOfData', 'subCentre',
        'paramIdECMF', 'paramId', 'cfNameECMF', 'cfName', 'cfVarNameECMF', 'cfVarName', 'unitsECMF', 'units', 'nameECMF',
        'name', 'decimalScaleFactor', 'setLocalDefinition', 'optimizeScaleFactor', 'dataDate', 'year', 'dataTime', 'julianDay',
        'stepUnits', 'stepType', 'stepRange', 'startStep', 'endStep', 'marsParam', 'validityDate', 'validityTime',
        'validityDateTime', 'deleteLocalDefinition', 'localUsePresent', 'shortNameECMF', 'shortName', 'ifsParam',
        'stepTypeForConversion', 'md5Section1', 'md5Product', 'paramIdForConversion', 'gridDescriptionSectionPresent',
        'bitmapPresent', 'angleSubdivisions', 'section2Length', 'radius', 'numberOfVerticalCoordinateValues', 'neitherPresent',
        'pvlLocation', 'dataRepresentationType', 'gridDefinitionDescription', 'gridDefinitionTemplateNumber', 'Ni', 'Nj',
        'latitudeOfFirstGridPoint', 'latitudeOfFirstGridPointInDegrees', 'longitudeOfFirstGridPoint', 
        'longitudeOfFirstGridPointInDegrees', 'resolutionAndComponentFlags', 'ijDirectionIncrementGiven', 'earthIsOblate', 
        'resolutionAndComponentFlags3', 'resolutionAndComponentFlags4', 'uvRelativeToGrid', 'resolutionAndComponentFlags6', 
        'resolutionAndComponentFlags7', 'resolutionAndComponentFlags8', 'latitudeOfLastGridPoint', 
        'latitudeOfLastGridPointInDegrees', 'longitudeOfLastGridPoint', 'longitudeOfLastGridPointInDegrees', 
        'iDirectionIncrement', 'jDirectionIncrement', 'isGridded', 'scanningMode', 'iScansNegatively', 'jScansPositively', 
        'jPointsAreConsecutive', 'alternativeRowScanning', 'iScansPositively', 'jScansNegatively', 'scanningMode4', 
        'scanningMode5', 'scanningMode6', 'scanningMode7', 'scanningMode8', 'swapScanningAlternativeRows', 
        'jDirectionIncrementInDegrees', 'iDirectionIncrementInDegrees', 'numberOfDataPoints', 'numberOfValues', 'latLonValues',
        'latitudes', 'longitudes', 'zeros', 'PVPresent', 'PLPresent', 'deletePV', 'md5Section2', 'isSpectral', 'lengthOfHeaders',
        'md5Headers', 'missingValue', 'tableReference', 'section4Length', 'halfByte', 'dataFlag', 'binaryScaleFactor', 
        'referenceValue', 'referenceValueError', 'sphericalHarmonics', 'complexPacking', 'integerPointValues', 
        'additionalFlagPresent', 'orderOfSPD', 'boustrophedonic', 'hideThis', 'packingType', 'bitsPerValue', 
        'constantFieldHalfByte', 'bitMapIndicator', 'values', 'numberOfCodedValues', 'packingError', 'unpackedError', 
        'maximum', 'minimum', 'average', 'standardDeviation', 'skewness', 'kurtosis', 'isConstant', 'numberOfMissing', 
        'dataLength', 'changeDecimalPrecision', 'decimalPrecision', 'bitsPerValueAndRepack', 'setPackingType', 
        'scaleValuesBy', 'offsetValuesBy', 'gridType', 'getNumberOfValues', 'md5Section4', 'section5Length'
    ]
    
    for key in keys:
        try:
            value = grb[key]
            logger.debug(f'{key}: {value}')
        except KeyError:
            logger.debug(f'{key}: Key not found')
        except Exception as e:
            logger.debug(f'Error retrieving {key}: {e}')

def process_grib_files(data_directory: str, flask_data_directory: str, global_min: float, global_max: float, 
                       display_specific_points: bool, specific_latitudes: List[float], specific_longitudes: List[float]) -> None:
    """
    Funkcja do przetwarzania plików GRIB w danym katalogu.

    Args:
        data_directory (str): Ścieżka do katalogu z plikami GRIB.
        flask_data_directory (str): Ścieżka do katalogu, gdzie zapisywane będą mapy ciepła.
        global_min (float): Globalna minimalna wartość temperatury.
        global_max (float): Globalna maksymalna wartość temperatury.
        display_specific_points (bool): Czy wyświetlać wartości temperatury w określonych punktach.
        specific_latitudes (list): Lista szerokości geograficznych, w których wyświetlać wartości.
        specific_longitudes (list): Lista długości geograficznych, w których wyświetlać wartości.
    """
    logger.info(f"Analizowanie danych z katalogu: {data_directory}")
    if not os.path.exists(data_directory):
        logger.error(f"Katalog {data_directory} nie istnieje.")
        return

    os.makedirs(flask_data_directory, exist_ok=True)
    logger.debug(f"Używając katalogu wyjściowego: {flask_data_directory}")

    files_processed = 0
    for filename in os.listdir(data_directory):
        if filename.startswith('.'):
            continue

        filepath = os.path.join(data_directory, filename)
        logger.debug(f"Przetwarzanie pliku: {filepath}")
        try:
            with pygrib.open(filepath) as grbs:
                for i, grb in enumerate(grbs):
                    if grb.parameterName != 'T Temperature K' or grb.level != 2:
                        logger.debug(f'Pomijanie rekordu {i+1} z pliku {filename} z powodu parametru: {grb.parameterName} i poziomu: {grb.level}')
                        continue
                    
                    lat, lon = grb.latlons()
                    data = grb.values - 273.15  # Konwersja z Kelwinów na Celsjusze

                    if lat.shape != lon.shape or lat.shape != data.shape:
                        logger.error(f"Liczba wartości ({data.size}) nie pasuje do liczby latitudes ({lat.size}) i longitudes ({lon.size})")
                        continue

                    # Logowanie szczegółowych informacji o kluczach i wartościach
                    logger.debug(f'Informacje o kluczach i wartościach dla pliku {filename}, rekord {i+1}:')
                    log_grib_keys(grb)

                    # Logowanie wartości temperatur
                    logger.debug(f'Próbka wartości temperatur z pliku {filename}, rekord {i+1}: {data.flatten()[:10]}')

                    # Generowanie mapy ciepła
                    latitudes = lat.flatten()
                    longitudes = lon.flatten()
                    values = data.flatten()
                    
                    param = grb.typeOfLevel

                    final_time, file_type, intervals = parse_filename(filename)
                    output_filename = f"{final_time.replace(' ', '_').replace(':', '')}_{i+1}_{param}_{grb.level}.png"
                    output_path = os.path.join(flask_data_directory, output_filename)
                    logger.debug(f'Output path for heatmap: {output_path}')
                    title = f'Mapa ciepła {final_time} {param} {grb.level}'

                    generate_heatmap(latitudes, longitudes, values, output_path, title, global_min, global_max, display_specific_points, specific_latitudes, specific_longitudes)
                    logger.info(f'Mapa ciepła została zapisana jako {output_path}')
                
                files_processed += 1
        except Exception as e:
            logger.error(f"Błąd podczas przetwarzania pliku {filepath} (plik: {filename}): {e}")
            raise

    if files_processed == 0:
        logger.info("Nie znaleziono żadnych plików GRIB do przetworzenia.")
    else:
        logger.info(f"Przetworzono {files_processed} plików GRIB.")

if __name__ == '__main__':
    try:
        global_min, global_max = find_global_min_max(data_directory)
        process_grib_files(data_directory, flask_data_directory, global_min, global_max, display_specific_points, specific_latitudes, specific_longitudes)
    except Exception as e:
        logger.critical(f"Niepowodzenie podczas przetwarzania plików GRIB: {e}")
