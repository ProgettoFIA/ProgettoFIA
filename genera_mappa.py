import pickle
from network import scarica_grafo

print("--- DOWNLOAD MAPPA IN CORSO ---")
grafo = scarica_grafo()
if grafo:
    with open("mappa_napoli.pkl", "wb") as f:
        pickle.dump(grafo, f)
    print("Fatto! Il file mappa_napoli.pkl è pronto.")