import logging
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree
from typing import List

logger = logging.getLogger('process_grib')

def find_nearest_points(latitudes: np.ndarray, longitudes: np.ndarray, specific_latitudes: List[float], specific_longitudes: List[float]):
    """
    Znajdź najbliższe punkty siatki do podanych specyficznych współrzędnych.

    Args:
        latitudes (np.ndarray): Tablica szerokości geograficznych.
        longitudes (np.ndarray): Tablica długości geograficznych.
        specific_latitudes (List[float]): Lista szerokości geograficznych, w których wyświetlać wartości.
        specific_longitudes (List[float]): Lista długości geograficznych, w których wyświetlać wartości.

    Returns:
        List[Tuple[float, float, int]]: Lista współrzędnych i indeksów dla najbliższych punktów.
    """
    points = np.column_stack((latitudes, longitudes))
    tree = cKDTree(points)
    
    nearest_points = []
    for lat in specific_latitudes:
        for lon in specific_longitudes:
            distance, index = tree.query([lat, lon])
            nearest_lat, nearest_lon = latitudes[index], longitudes[index]
            nearest_points.append((nearest_lat, nearest_lon, index))

    return nearest_points

def generate_heatmap(latitudes: np.ndarray, longitudes: np.ndarray, values: np.ndarray, output_path: str, title: str, 
                     global_min: float, global_max: float, display_specific_points: bool, specific_latitudes: List[float], 
                     specific_longitudes: List[float]) -> None:
    """
    Generowanie mapy ciepła z danych.

    Args:
        latitudes (np.ndarray): Tablica szerokości geograficznych.
        longitudes (np.ndarray): Tablica długości geograficznych.
        values (np.ndarray): Tablica wartości.
        output_path (str): Ścieżka do pliku wyjściowego.
        title (str): Tytuł mapy ciepła.
        global_min (float): Globalna minimalna wartość temperatury.
        global_max (float): Globalna maksymalna wartość temperatury.
        display_specific_points (bool): Czy wyświetlać wartości temperatury w określonych punktach.
        specific_latitudes (list): Lista szerokości geograficznych, w których wyświetlać wartości.
        specific_longitudes (list): Lista długości geograficznych, w których wyświetlać wartości.
    """
    logger.debug(f'Generating heatmap with {len(latitudes)} points.')
    logger.debug(f'Global min: {global_min}, Global max: {global_max}')

    plt.figure(figsize=(10, 8))
    contour = plt.tricontourf(longitudes, latitudes, values, levels=np.linspace(global_min, global_max, 100), cmap='jet')
    plt.colorbar(contour)
    plt.title(title)

    if display_specific_points:
        nearest_points = find_nearest_points(latitudes, longitudes, specific_latitudes, specific_longitudes)
        for nearest_lat, nearest_lon, index in nearest_points:
            plt.text(nearest_lon, nearest_lat, f'{values[index]:.1f}', ha='center', va='center', fontsize=8, color='black')
            logger.debug(f'Added text at ({nearest_lon}, {nearest_lat}): {values[index]:.1f}')

    plt.savefig(output_path)
    plt.close()

    logger.debug(f'Heatmap saved to {output_path}')
