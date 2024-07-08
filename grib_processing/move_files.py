import os
import yaml
import shutil

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
    'surface_1.png': '1_surface_0',
    # Dodaj więcej wzorców jeśli potrzebne
    'heightAboveGround_2_5.png': '5_heightAboveGround_2',
    'isobaricInhPa_100.png': '29_isobaricInhPa_100',
    'heightAboveGround_2_7.png': '7_heightAboveGround_2',
    'heightAboveGround_2_8.png': '8_heightAboveGround_2',
    'isobaricInhPa_300.png': '30_isobaricInhPa_300',
    'isobaricInhPa_500.png': '31_isobaricInhPa_500',
    'isobaricInhPa_700.png': '36_isobaricInhPa_700',
    'isobaricInhPa_850.png': '33_isobaricInhPa_850',
    'isobaricInhPa_925.png': '34_isobaricInhPa_925',
}

def move_files(source_directory=source_dir, target_directory=None, file_map=file_mapping):
    """Przenoszenie plików z katalogu źródłowego do odpowiednich podkatalogów."""
    target_directory = target_directory or source_directory
    
    for filename in os.listdir(source_directory):
        for pattern, subdir in file_map.items():
            if pattern in filename:
                target_dir = os.path.join(target_directory, subdir)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                shutil.move(os.path.join(source_directory, filename), os.path.join(target_dir, filename))
                print(f"Przeniesiono plik z {os.path.join(source_directory, filename)} do {os.path.join(target_dir, filename)}")
                break

if __name__ == '__main__':
    move_files()
