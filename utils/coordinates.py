import numpy as np


def converti_latlon_to_mercator(lat, lon):
    """Converte GPS (lat/lon) in coordinate(X,Y) per lo sfondo della mappa."""
    # Equatore espresso in metri
    r_major = 6378137.000
    x = r_major * np.radians(lon)
    scale = x / lon
    y = 180.0 / np.pi * np.log(np.tan(np.pi / 4.0 + lat * (np.pi / 180.0) / 2.0)) * scale
    return x, y
