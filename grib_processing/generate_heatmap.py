import numpy as np
import matplotlib.pyplot as plt

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
