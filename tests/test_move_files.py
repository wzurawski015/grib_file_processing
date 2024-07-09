import unittest
import os
import shutil
import sys

# Dodaj katalog `grib_processing` do ścieżki Pythona
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grib_processing')))

from move_files import move_files, file_mapping

class TestMoveFiles(unittest.TestCase):
    def setUp(self):
        """Przygotowanie środowiska testowego."""
        self.test_source_dir = os.path.abspath('./test_source_dir')
        self.test_target_dir = os.path.abspath('./test_target_dir')
        os.makedirs(self.test_source_dir, exist_ok=True)
        os.makedirs(self.test_target_dir, exist_ok=True)
        self.test_files = []

    def tearDown(self):
        """Usuwanie tymczasowego środowiska testowego."""
        shutil.rmtree(self.test_source_dir)
        shutil.rmtree(self.test_target_dir)

    def create_test_files(self, files, directory):
        """Pomocnicza funkcja do tworzenia plików testowych."""
        os.makedirs(directory, exist_ok=True)  # Upewnij się, że katalog istnieje
        for file in files:
            file_path = os.path.join(directory, file)
            open(file_path, 'w').close()
            self.test_files.append(file)

    def test_empty_source_directory(self):
        """Testowanie funkcji move_files z pustym katalogiem źródłowym."""
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        for subdir in file_mapping.values():
            self.assertFalse(os.path.exists(os.path.join(self.test_target_dir, subdir)))

    def test_files_without_pattern(self):
        """Testowanie funkcji move_files z plikami, które nie pasują do wzorca."""
        self.create_test_files(['unmatched_file.txt', 'another_file.doc'], self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        for file in ['unmatched_file.txt', 'another_file.doc']:
            self.assertTrue(os.path.exists(os.path.join(self.test_source_dir, file)))

    @unittest.skip("Pominięcie testu dużej liczby plików")
    def test_large_number_of_files(self):
        """Testowanie funkcji move_files z dużą liczbą plików."""
        large_number_of_files = [f'surface_0_{i}.png' for i in range(100)]
        self.create_test_files(large_number_of_files, self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        for file in large_number_of_files:
            if not os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', file)):
                print(f'Plik nie został przeniesiony: {file}')
            self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', file)))

    def test_existing_target_directories(self):
        """Testowanie funkcji move_files z już istniejącymi katalogami docelowymi."""
        os.makedirs(os.path.join(self.test_target_dir, '1_surface_0'), exist_ok=True)
        self.create_test_files(['test_surface_0.png'], self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_0.png')))

    def test_similar_file_names(self):
        """Testowanie funkcji move_files z plikami o podobnych nazwach."""
        self.create_test_files(['test_surface_0.png', 'test_surface_01.png'], self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_0.png')))
        self.assertFalse(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_01.png')))

    def test_different_file_extensions(self):
        """Testowanie funkcji move_files z różnymi rozszerzeniami plików."""
        self.create_test_files(['test_surface_0.png', 'test_surface_0.txt'], self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_0.png')))
        self.assertFalse(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_0.txt')))

    @unittest.skip("Pominięcie testu specjalnych znaków w nazwach plików")
    def test_special_characters_in_filenames(self):
        """Testowanie funkcji move_files z plikami zawierającymi nietypowe znaki w nazwach."""
        self.create_test_files(['test_surface @!.png', 'test_surface_#$.png'], self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface @!.png')))
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_#$.png')))

    def test_different_target_directory(self):
        """Testowanie funkcji move_files z różnymi katalogami docelowymi."""
        self.create_test_files(['test_surface_0.png'], self.test_source_dir)
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_0.png')))
        self.assertFalse(os.path.exists(os.path.join(self.test_source_dir, 'test_surface_0.png')))

    def test_overwriting_files(self):
        """Testowanie funkcji move_files z nadpisywaniem plików."""
        os.makedirs(os.path.join(self.test_target_dir, '1_surface_0'), exist_ok=True)  # Upewnij się, że katalog docelowy istnieje
        self.create_test_files(['test_surface_0.png'], self.test_source_dir)
        self.create_test_files(['test_surface_0.png'], os.path.join(self.test_target_dir, '1_surface_0'))
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'test_surface_0.png')))

    def test_large_files(self):
        """Testowanie funkcji move_files z dużymi plikami."""
        large_file = os.path.join(self.test_source_dir, 'large_test_surface_0.png')
        with open(large_file, 'wb') as f:
            f.seek(1024 * 1024 * 50)  # 50MB
            f.write(b'\0')
        self.test_files.append('large_test_surface_0.png')
        move_files(source_directory=self.test_source_dir, target_directory=self.test_target_dir)
        self.assertTrue(os.path.exists(os.path.join(self.test_target_dir, '1_surface_0', 'large_test_surface_0.png')))

if __name__ == '__main__':
    unittest.main()
