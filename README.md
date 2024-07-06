# grib_file_processing
## Opis projektu

Projekt ten ma na celu analizę i wizualizację danych meteorologicznych zapisanych w plikach GRIB edition 1 przy użyciu bibliotek ecCodes, Flask, htmx oraz Docker. Projekt generuje mapy ciepła i serwuje je jako dynamicznie zmieniające się obrazy na stronie internetowej.

## Struktura projektu

- `app.py`: Główna aplikacja Flask, serwująca dynamicznie zmieniające się obrazy map ciepła.
- `config.yaml`: Plik konfiguracyjny zawierający ustawienia ścieżek, interwałów czasu itp.
- `generate_heatmaps.py`: Skrypt generujący mapy ciepła bezpośrednio z plików GRIB.
- `index.html`: Szablon HTML do wyświetlania obrazów map ciepła.

## Instalacja i uruchomienie

1. **Klonowanie repozytorium**:
    ```sh
    git clone https://github.com/wzurawski015/grib_file_processing.git
    cd grib_file_processing
    ```

2. **Utworzenie i aktywacja wirtualnego środowiska**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Instalacja zależności**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Konfiguracja ścieżek w pliku `config.yaml`**:
    Upewnij się, że ścieżki w pliku `config.yaml` są poprawne.

5. **Uruchomienie aplikacji Flask**:
    ```sh
    python app.py
    ```

Po wykonaniu tych kroków aplikacja Flask powinna działać i serwować dynamicznie zmieniające się mapy ciepła na stronie internetowej.
