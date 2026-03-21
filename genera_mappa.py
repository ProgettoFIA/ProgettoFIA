import pickle
from network import scarica_grafo, zoneRosse

print("--- DOWNLOAD MAPPA IN CORSO ---")
grafo = scarica_grafo()
if grafo:
    grafo = zoneRosse(grafo, crater_lat=40.8224, crater_lon=14.4289, raggio_km=4.5)
    with open("mappa_napoli.pkl", "wb") as f:
        pickle.dump(grafo, f)
    print("Fatto! Il file mappa_napoli.pkl è pronto.")