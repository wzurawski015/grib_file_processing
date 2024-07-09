import os
import yaml
import shutil
import logging

# Konfiguracja logowania
logging.basicConfig(filename='file_operations.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Ścieżka do pliku konfiguracyjnego
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.yaml'))

# Wczytaj plik konfiguracyjny
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Ścieżki katalogów
source_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', config['data_directory_flask']))

# Mapowanie wzorców plików na podkatalogi
file_mapping = {
    'surface_0.png': '1_surface_0',
#    'heightAboveGround_2_5.png': '5_heightAboveGround_2',
    'isobaricInhPa_100.png': '29_isobaricInhPa_100',
#    'heightAboveGround_2_7.png': '7_heightAboveGround_2',
    'heightAboveGround_2.png': '8_heightAboveGround_2',
    'isobaricInhPa_300.png': '30_isobaricInhPa_300',
    'isobaricInhPa_500.png': '31_isobaricInhPa_500',
    'isobaricInhPa_700.png': '36_isobaricInhPa_700',
    'isobaricInhPa_850.png': '33_isobaricInhPa_850',
    'isobaricInhPa_925.png': '34_isobaricInhPa_925',
}

def move_files(source_directory=source_dir, target_directory=None, file_map=file_mapping, operation='move'):
    """Przenoszenie lub kopiowanie plików z katalogu źródłowego do odpowiednich podkatalogów."""
    target_directory = target_directory or source_directory
    
    for filename in os.listdir(source_directory):
        try:
            for pattern, subdir in file_map.items():
                if filename.endswith(pattern):
                    target_dir = os.path.join(target_directory, subdir)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    
                    src_path = os.path.join(source_directory, filename)
                    dest_path = os.path.join(target_dir, filename)
                    
                    if operation == 'move':
                        shutil.move(src_path, dest_path)
                        logging.info(f'Przeniesiono plik z {src_path} do {dest_path}')
                    elif operation == 'copy':
                        shutil.copy2(src_path, dest_path)
                        logging.info(f'Skopiowano plik z {src_path} do {dest_path}')
                    print(f"Operacja {operation} plik z {src_path} do {dest_path}")
                    break
        except Exception as e:
            logging.error(f'Błąd podczas operacji na pliku {filename}: {e}')
            print(f'Błąd podczas operacji na pliku {filename}: {e}')

if __name__ == '__main__':
    move_files(operation='move')  # Można zmienić na 'copy' dla kopiowania plików
