# Ścieżka: tests/test_move_files.py

import os
import unittest
import shutil
from unittest.mock import patch
import sys

# Dodajemy ścieżkę do grib_processing, aby umożliwić importowanie modułów
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grib_processing')))

from move_files import move_files, file_mapping

class TestMoveFiles(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Tworzenie tymczasowej struktury katalogów do testów."""
        cls.test_source_dir = 'test_data/meteo'
        cls.test_target_dir = 'test_data/flask_data'

        # Tworzenie katalogu źródłowego
        os.makedirs(cls.test_source_dir, exist_ok=True)
        # Tworzenie plików testowych w katalogu źródłowym
        for suffix in file_mapping.keys():
            with open(os.path.join(cls.test_source_dir, f'testfile{suffix}'), 'w') as f:
                f.write('test')

    @classmethod
    def tearDownClass(cls):
        """Usuwanie tymczasowej struktury katalogów po testach."""
        shutil.rmtree('test_data')

    @patch.dict('move_files.config', {'source_directory': 'test_data/meteo', 'target_directory': 'test_data/flask_data'})
    def test_move_files(self):
        """Testowanie funkcji move_files."""
        # Uruchamianie funkcji move_files
        move_files('test_data/meteo', 'test_data/flask_data')

        # Sprawdzanie, czy pliki zostały przeniesione do odpowiednich katalogów
        for suffix, target_subdir in file_mapping.items():
            target_path = os.path.join(self.test_target_dir, target_subdir, f'testfile{suffix}')
            self.assertTrue(os.path.exists(target_path), f'Plik {target_path} nie został znaleziony')

if __name__ == '__main__':
    unittest.main()
