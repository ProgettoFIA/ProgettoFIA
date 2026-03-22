import math
from typing import Tuple, Callable

# Costanti per i tipi di euristica
EURISTICA_EUCLIDEA = "euclidea"
EURISTICA_MANHATTAN = "manhattan"
EURISTICA_CHEBYSHEV = "chebyshev"


def calcola_distanza_euclidea(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    lat_media = math.radians((pos1[0] + pos2[0]) / 2)
    dy = (pos2[0] - pos1[0]) * 111139
    dx = (pos2[1] - pos1[1]) * 111139 * math.cos(lat_media)
    return math.sqrt(dx * dx + dy * dy)


def calcola_distanza_manhattan(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    lat_media = math.radians((pos1[0] + pos2[0]) / 2)
    dy = abs(pos2[0] - pos1[0]) * 111139
    dx = abs(pos2[1] - pos1[1]) * 111139 * math.cos(lat_media)
    return dx + dy


def calcola_distanza_chebyshev(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    lat_media = math.radians((pos1[0] + pos2[0]) / 2)
    dy = abs(pos2[0] - pos1[0]) * 111139
    dx = abs(pos2[1] - pos1[1]) * 111139 * math.cos(lat_media)
    return max(dx, dy)

# Restituisce la funzione euristica corrispondente al tipo scelto
def get_funzione_euristica(tipo_euristica: str) -> Callable[[Tuple[float, float], Tuple[float, float]], float]:
    if tipo_euristica == EURISTICA_EUCLIDEA:
        return calcola_distanza_euclidea
    elif tipo_euristica == EURISTICA_MANHATTAN:
        return calcola_distanza_manhattan
    elif tipo_euristica == EURISTICA_CHEBYSHEV:
        return calcola_distanza_chebyshev
    else:
        raise ValueError(f"Tipo di euristica non supportato: {tipo_euristica}")
