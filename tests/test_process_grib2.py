import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import logging
import io

# Dodaj ścieżkę do katalogu `grib_processing` do ścieżki Pythona
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'grib_processing')))

from process_grib import parse_filename, process_grib_files

class TestProcessGrib(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger('process_grib')
        self.logger.setLevel(logging.ERROR)
        self.log_capture_string = io.StringIO()
        ch = logging.StreamHandler(self.log_capture_string)
        ch.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)
        self.addCleanup(self.cleanup_logger)

    def cleanup_logger(self):
        self.logger.handlers = []

    def tearDown(self):
        logging.disable(logging.NOTSET)  # Włącz logowanie po zakończeniu testów

    def test_parse_filename_valid(self):
        """Testowanie poprawnego parsowania nazw plików GRIB."""
        filename = 'fc20230701_00+012gl'
        expected_result = ('2023-07-01 01:00', 'gl', '012')
        result = parse_filename(filename)
        self.assertEqual(result, expected_result)

    def test_parse_filename_valid_different_intervals(self):
        """Testowanie poprawnego parsowania nazw plików GRIB z różnymi interwałami."""
        filename = 'fc20230701_00+006gl'
        expected_result = ('2023-07-01 00:30', 'gl', '006')
        result = parse_filename(filename)
        self.assertEqual(result, expected_result)

    def test_parse_filename_invalid(self):
        """Testowanie parsowania niepoprawnych nazw plików GRIB."""
        filename = 'invalid_filename'
        with self.assertRaises(ValueError):
            parse_filename(filename)

    @patch('process_grib.pygrib.open')
    @patch('os.listdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_process_grib_files(self, mock_path_join, mock_listdir, mock_pygrib_open):
        """Testowanie przetwarzania plików GRIB."""
        mock_listdir.return_value = ['test1.grb', 'test2.grb']
        mock_grb = MagicMock()
        mock_grb.__iter__.return_value = [mock_grb, mock_grb]
        mock_pygrib_open.return_value = mock_grb

        with patch('builtins.print') as mocked_print:
            process_grib_files('dummy_directory')
            self.assertEqual(mock_pygrib_open.call_count, 2)
            self.assertTrue(mocked_print.called)

    @patch('process_grib.pygrib.open')
    @patch('os.listdir')
    def test_process_grib_files_no_grb_files(self, mock_listdir, mock_pygrib_open):
        """Testowanie przetwarzania gdy brak plików GRIB."""
        mock_listdir.return_value = ['file1.txt', 'file2.doc']
        process_grib_files('dummy_directory')
        mock_pygrib_open.assert_not_called()

    @patch('process_grib.pygrib.open', side_effect=Exception('Internal Error'))
    @patch('os.listdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_process_grib_files_internal_error(self, mock_path_join, mock_listdir, mock_pygrib_open):
        """Testowanie przetwarzania plików GRIB z błędem wewnętrznym."""
        mock_listdir.return_value = ['test1.grb']
        with self.assertRaises(Exception):
            process_grib_files('dummy_directory')
        log_contents = self.log_capture_string.getvalue()
        print("Log output:", log_contents)  # Debugowanie logów
        self.assertIn('Błąd podczas przetwarzania pliku', log_contents)

    @patch('os.listdir', side_effect=FileNotFoundError('Directory not found'))
    def test_process_grib_files_directory_not_found(self, mock_listdir):
        """Testowanie przetwarzania gdy katalog nie istnieje."""
        with self.assertRaises(FileNotFoundError):
            process_grib_files('dummy_directory')

    @patch('os.listdir')
    def test_process_grib_files_empty_directory(self, mock_listdir):
        """Testowanie przetwarzania gdy katalog jest pusty."""
        mock_listdir.return_value = []
        process_grib_files('dummy_directory')
        log_contents = self.log_capture_string.getvalue()
        self.assertEqual(log_contents, '')  # No logs should be generated for empty directory

    @patch('process_grib.pygrib.open')
    @patch('os.listdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_process_grib_files_mixed_files(self, mock_path_join, mock_listdir, mock_pygrib_open):
        """Testowanie przetwarzania plików GRIB i nie-GRIB w jednym katalogu."""
        mock_listdir.return_value = ['valid.grb', 'invalid.txt']
        mock_grb = MagicMock()
        mock_grb.__iter__.return_value = [mock_grb, mock_grb]
        mock_pygrib_open.return_value = mock_grb

        with patch('builtins.print') as mocked_print:
            process_grib_files('dummy_directory')
            self.assertEqual(mock_pygrib_open.call_count, 1)
            self.assertTrue(mocked_print.called)
        log_contents = self.log_capture_string.getvalue()
        self.assertNotIn('invalid.txt', log_contents)

    @patch('process_grib.pygrib.open')
    @patch('os.listdir')
    @patch('os.path.join', side_effect=lambda *args: '/'.join(args))
    def test_process_grib_files_large_number_of_files(self, mock_path_join, mock_listdir, mock_pygrib_open):
        """Testowanie przetwarzania dużej liczby plików GRIB."""
        mock_listdir.return_value = [f'test{i}.grb' for i in range(1000)]
        mock_grb = MagicMock()
        mock_grb.__iter__.return_value = [mock_grb, mock_grb]
        mock_pygrib_open.return_value = mock_grb

        with patch('builtins.print') as mocked_print:
            process_grib_files('dummy_directory')
            self.assertEqual(mock_pygrib_open.call_count, 1000)
            self.assertTrue(mocked_print.called)

if __name__ == '__main__':
    unittest.main()
