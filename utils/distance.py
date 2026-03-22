import math


def dist_metri(lat1, lon1, lat2, lon2):
    """Calcola distanza in metri."""
    dx = (lon1 - lon2) * 111000 * math.cos(math.radians((lat1 + lat2) / 2))
    dy = (lat1 - lat2) * 111000
    return math.sqrt(dx * dx + dy * dy)
