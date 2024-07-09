import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Ustawienie backendu 'Agg' dla Matplotlib
matplotlib.use('Agg')

def generate_heatmap(latitudes, longitudes, values, output_path, title):
    """
    Generuje mapę ciepła i zapisuje ją jako plik PNG.

    Args:
        latitudes (np.array): Tablica szerokości geograficznych.
        longitudes (np.array): Tablica długości geograficznych.
        values (np.array): Tablica wartości temperatury.
        output_path (str): Ścieżka do pliku wyjściowego.
        title (str): Tytuł mapy ciepła.
    """
    # Sprawdzenie, czy liczba wartości pasuje do liczby latitudes i longitudes
    if len(values) != len(latitudes) * len(longitudes):
        raise ValueError("Liczba wartości nie pasuje do liczby latitudes i longitudes")

    plt.figure(figsize=(10, 8))
    plt.imshow(values.reshape(len(latitudes), len(longitudes)), cmap='coolwarm', interpolation='nearest')
    plt.title(title)
    plt.colorbar()
    plt.savefig(output_path)
    plt.close()

# Przykładowe wywołanie funkcji
if __name__ == '__main__':
    # Przykładowe dane
    latitudes = np.linspace(-90, 90, 180)
    longitudes = np.linspace(-180, 180, 360)
    values = np.random.rand(len(latitudes) * len(longitudes))

    # Ścieżka do pliku wyjściowego
    output_path = 'heatmap.png'
    title = 'Przykładowa mapa ciepła'

    generate_heatmap(latitudes, longitudes, values, output_path, title)
    print(f'Mapa ciepła została zapisana jako {output_path}')
