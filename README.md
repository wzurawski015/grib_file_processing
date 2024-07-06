EADME.md dla projektu grib_file_processing:

grib_file_processing/
├── config.yaml # Plik konfiguracyjny dla ścieżek i ustawień
├── docker-compose.yml # Konfiguracja Docker Compose
├── flask_app/ # Aplikacja Flask do serwowania map ciepła
│ ├── app.py # Główny skrypt aplikacji Flask
│ ├── static/ # Pliki statyczne (np. CSS, JavaScript)
│ ├── templates/ # Szablony HTML
│ ├── venv_flask/ # Wirtualne środowisko dla aplikacji Flask
│ └── requirements.txt # Zależności Python dla aplikacji Flask
├── grib_processing/ # Skrypty do przetwarzania plików GRIB
│ ├── process_grib.py # Skrypt do przetwarzania plików GRIB i generowania map ciepła
│ ├── generate_heatmap.py # Skrypt do generowania map ciepła
│ ├── move_files.py # Skrypt do przenoszenia plików PNG do katalogu docelowego
│ ├── venv_grib/ # Wirtualne środowisko dla przetwarzania GRIB
│ └── requirements.txt # Zależności Python dla przetwarzania GRIB
├── tests/ # Testy jednostkowe
│ ├── test_process_grib.py
│ └── test_generate_heatmaps.py
└── README.md # Dokumentacja projektu


## Konfiguracja

Plik `config.yaml` zawiera konfigurację ścieżek i ustawień:

```yaml
data_directory: "../data/meteo"
target_directory: "../data/flask_data/1_surface_0"
htmx:
  trigger_interval: "1s"


#Instalacja i uruchomienie
Pobranie repozytorium
Pobierz repozytorium z GitHub:

git clone https://github.com/yourusername/grib_file_processing.git
cd grib_file_processing

#Wirtualne środowisko dla grib_processing
#Utwórz i aktywuj wirtualne środowisko dla grib_processing:

cd grib_processing
python3 -m venv venv_grib
source venv_grib/bin/activate
pip install -r requirements.txt

#Wirtualne środowisko dla flask_app
#Utwórz i aktywuj wirtualne środowisko dla flask_app:

cd ../flask_app
python3 -m venv venv_flask
source venv_flask/bin/activate
pip install -r requirements.txt

#Uruchomienie aplikacji Flask
#Uruchom aplikację Flask:
cd flask_app
source venv_flask/bin/activate
python app.py

#Przetwarzanie plików GRIB i generowanie map ciepła
#Przetwórz pliki GRIB i wygeneruj mapy ciepła:
cd ../grib_processing
source venv_grib/bin/activate
python move_files.py
python process_grib.py

#Testowanie jednostkowe
#Uruchom testy jednostkowe:
cd ../tests
source venv_grib/bin/activate
export PYTHONPATH=$PYTHONPATH:$(pwd)/../grib_processing
python -m unittest test_process_grib.py
python -m unittest test_generate_heatmaps.py

#Docker
#Docker Compose
#Projekt zawiera plik docker-compose.yml, który pozwala na uruchomienie aplikacji za pomocą Docker Compose.
#Budowanie i uruchamianie za pomocą Docker Compose
#Aby zbudować i uruchomić kontenery, użyj poniższych poleceń:
docker-compose build
docker-compose up

#Kontenery zostaną uruchomione zgodnie z konfiguracją w docker-compose.yml.
#Ten projekt jest wciąż w fazie rozwoju. Zachęcamy do zgłaszania błędów oraz propozycji usprawnień poprzez system zgłoszeń na GitHubie.
#Dziękujemy za korzystanie z grib_file_processing!


