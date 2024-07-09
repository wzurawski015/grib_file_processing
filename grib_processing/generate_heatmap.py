import logging
import matplotlib.pyplot as plt

logger = logging.getLogger('process_grib')

def generate_heatmap(latitudes, longitudes, values, output_path, title):
    """
    Generowanie mapy ciepła z danych.

    Args:
        latitudes (np.ndarray): Tablica szerokości geograficznych.
        longitudes (np.ndarray): Tablica długości geograficznych.
        values (np.ndarray): Tablica wartości.
        output_path (str): Ścieżka do pliku wyjściowego.
        title (str): Tytuł mapy ciepła.
    """
    logger.debug(f'Generating heatmap with {len(latitudes)} points.')

    plt.figure(figsize=(10, 8))
    plt.tricontourf(longitudes, latitudes, values, levels=100, cmap='jet')
    plt.colorbar()
    plt.title(title)
    plt.savefig(output_path)
    plt.close()

    logger.debug(f'Heatmap saved to {output_path}')
