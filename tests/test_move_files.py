# Ścieżka: tests/test_move_files.py

import os
import unittest
import shutil
from unittest.mock import patch
from grib_processing.move_files import move_files

class TestMoveFiles(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Tworzenie tymczasowej struktury katalogów do testów."""
        cls.test_source_dir = 'test_data/meteo'
        cls.test_target_dir = 'test_data/flask_data'
        cls.file_mapping = {
            '_1_surface_0.png': '1_surface_0',
            '_5_heightAboveGround_2.png': '5_heightAboveGround_2',
            '_29_isobaricInhPa_100.png': '29_isobaricInhPa_100',
            '_7_heightAboveGround_2.png': '7_heightAboveGround_2',
            '_8_heightAboveGround_2.png': '8_heightAboveGround_2',
            '_30_isobaricInhPa_300.png': '30_isobaricInhPa_300',
            '_31_isobaricInhPa_500.png': '31_isobaricInhPa_500',
            '_32_isobaricInhPa_700.png': '32_isobaricInhPa_700',
            '_33_isobaricInhPa_850.png': '33_isobaricInhPa_850',
            '_34_isobaricInhPa_925.png': '34_isobaricInhPa_925'
        }

        # Tworzenie katalogu źródłowego
        os.makedirs(cls.test_source_dir, exist_ok=True)
        # Tworzenie plików testowych w katalogu źródłowym
        for suffix in cls.file_mapping.keys():
            with open(os.path.join(cls.test_source_dir, f'testfile{suffix}'), 'w') as f:
                f.write('test')

    @classmethod
    def tearDownClass(cls):
        """Usuwanie tymczasowej struktury katalogów po testach."""
        shutil.rmtree('test_data')

    @patch('grib_processing.move_files.config')
    def test_move_files(self, mock_config):
        """Testowanie funkcji move_files."""
        mock_config['source_directory'] = self.test_source_dir
        mock_config['target_directory'] = self.test_target_dir

        # Uruchamianie funkcji move_files
        move_files()

        # Sprawdzanie, czy pliki zostały przeniesione do odpowiednich katalogów
        for suffix, target_subdir in self.file_mapping.items():
            target_path = os.path.join(self.test_target_dir, target_subdir, f'testfile{suffix}')
            self.assertTrue(os.path.exists(target_path), f'Plik {target_path} nie został znaleziony')

if __name__ == '__main__':
    unittest.main()
