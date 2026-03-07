import networkx as nx
from utils import dist_metri
from network import get_nearest_node
import time

def scegli_rifugio_migliore(G, famiglia, lista_rifugi, algoritmo= "A*"):
    nodo_start = get_nearest_node(G, famiglia.lat, famiglia.lon)

    miglior_rifugio = None
    miglior_percorso = []
    min_tempo = float('inf')

    #per misurare il tempo di esecuzione dell'algoritmo per poi confrontarlo useremo un timer
    start_algoritmo=time.time()
    print(f"\n🔍 Analisi per {famiglia.nome} ({famiglia.descrizione})...")

    for rifugio in lista_rifugi:
        nodo_end = rifugio.nodo_grafo
        try:
            # Euristica per A*
            def euristica(u, v):
                pos_u = G.nodes[u]['pos']
                pos_v = G.nodes[v]['pos']
                return dist_metri(pos_u[0], pos_u[1], pos_v[0], pos_v[1])

            #scegliamo l'algoritmo di ricerca
            if(algoritmo== "A*"):

                # Calcolo percorso con A*
                percorso_temp = nx.astar_path(G, source=nodo_start, target=nodo_end,
                                          heuristic=euristica, weight='weight')
            elif algoritmo=="dijkstra":

                percorso_temp=nx.dijkstra_path(
                    G,
                    source=nodo_start,
                    target=nodo_end,
                    weight='weight'
                )
            else:
                raise ValueError("Algoritmo non supportato")

            path_len = nx.path_weight(G, percorso_temp, weight='weight')
            tempo_minuti = (path_len / famiglia.speed_ms) / 60

            print(f"   -> Verso {rifugio.nome}: {path_len / 1000:.1f} km ({tempo_minuti:.0f} min)")

            if tempo_minuti < min_tempo:
                min_tempo = tempo_minuti
                miglior_rifugio = rifugio
                miglior_percorso = percorso_temp

        except nx.NetworkXNoPath:
            print(f"   -> {rifugio.nome}: NON RAGGIUNGIBILE")

    tempo_esecuzione=time.time() - start_algoritmo

    print(f"Algoritmo {algoritmo.upper()} completato in {tempo_esecuzione:.4f} secondi")
    return miglior_rifugio, miglior_percorso, min_tempo, tempo_esecuzione
