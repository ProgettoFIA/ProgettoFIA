import networkx as nx
from utils import dist_metri
from network import get_nearest_node
import time
import heapq
import math
from typing import Dict, List, Optional, Tuple, Callable

# Costanti per i tipi di euristica
EURISTICA_EUCLIDEA = "euclidea"
EURISTICA_MANHATTAN = "manhattan"
EURISTICA_CHEBYSHEV = "chebyshev"

#Calcola la distanza euclidea tra due punti
def calcola_distanza_euclidea(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

#Calcola la distanza di Manhattan tra due punti
def calcola_distanza_manhattan(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

#Calcola la distanza di Chebyshev tra due punti
def calcola_distanza_chebyshev(pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
    return max(abs(pos2[0] - pos1[0]), abs(pos2[1] - pos1[1]))

#Restituisce la funzione euristica corrispondente al tipo scelto
def get_funzione_euristica(tipo_euristica: str) -> Callable[[Tuple[float, float], Tuple[float, float]], float]:
    if tipo_euristica == EURISTICA_EUCLIDEA:
        return calcola_distanza_euclidea
    elif tipo_euristica == EURISTICA_MANHATTAN:
        return calcola_distanza_manhattan
    elif tipo_euristica == EURISTICA_CHEBYSHEV:
        return calcola_distanza_chebyshev
    else:
        raise ValueError(f"Tipo di euristica non supportato: {tipo_euristica}")

#Implementazione personalizzata dell'algoritmo A* con diverse euristiche che restituisce una lista che contiene il percorso ottimale
def a_star_search_personalizzato(G: nx.Graph,
                                 source: str,
                                 target: str,
                                 tipo_euristica: str = EURISTICA_EUCLIDEA,
                                 weight: str = 'weight') -> List[str]:

    # Ottieni la funzione euristica selezionata
    funzione_dist = get_funzione_euristica(tipo_euristica)

    #Calcola la distanza tra due nodi usando l'euristica scelta
    def euristica(u: str, v: str) -> float:

        pos_u = G.nodes[u]['pos']
        pos_v = G.nodes[v]['pos']
        return funzione_dist(pos_u, pos_v)

    # Insieme dei nodi già esplorati
    closed_set = set()

    # Dizionario per tracciare il nodo precedente nel percorso ottimale
    came_from: Dict[str, Optional[str]] = {}

    # Dizionario per memorizzare il costo effettivo dal nodo start a ciascun nodo
    g_score: Dict[str, float] = {source: 0.0}

    # Dizionario per memorizzare il costo totale stimato
    f_score: Dict[str, float] = {source: euristica(source, target)}

    open_set = [(f_score[source], g_score[source], source)]
    open_set_nodes = {source}

    # Conteggio dei nodi esplorati
    nodi_esplorati = 0

    while open_set:
        # Estrai il nodo con f_score minimo
        current_f, current_g, current = heapq.heappop(open_set)
        open_set_nodes.remove(current)
        nodi_esplorati += 1

        # Se il nodo corrente è il nodo target, restituisce il percorso
        if current == target:
            return ricostruisci_percorso(came_from, current)

        # Aggiungi il nodo corrente all'insieme dei chiusi
        closed_set.add(current)

        # Esplora tutti i vicini del nodo corrente
        for neighbor in G.neighbors(current):
            if neighbor in closed_set:
                continue

            # Calcola il costo del percorso dal nodo corrente al vicino
            edge_data = G.get_edge_data(current, neighbor)
            edge_weight = edge_data.get(weight, 1.0) if edge_data else 1.0

            tentative_g_score = g_score[current] + edge_weight

            # Se il vicino non è stato ancora visitato o abbiamo trovato un percorso migliore
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                f_score[neighbor] = tentative_g_score + euristica(neighbor, target)

                # Aggiungi alla coda di priorità se non è già presente
                if neighbor not in open_set_nodes:
                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
                    open_set_nodes.add(neighbor)

    raise nx.NetworkXNoPath(f"Nessun percorso trovato tra {source} e {target}")

#Ricostruisce il percorso dalla fonte al nodo corrente
def ricostruisci_percorso(came_from: Dict[str, Optional[str]], current: str) -> List[str]:

    total_path = [current]
    while current in came_from:
        current = came_from[current]
        if current is not None:
            total_path.append(current)
    total_path.reverse()
    return total_path

def scegli_rifugio_migliore(G, famiglia, lista_rifugi, algoritmo="A*", tipo_euristica="euclidea"):
    nodo_start = get_nearest_node(G, famiglia.lat, famiglia.lon)
    miglior_rifugio = None
    miglior_percorso = []
    min_tempo = float('inf')

    #Scelta dell'euristica
    if algoritmo == "A*":
        print(f"\nAnalisi per {famiglia.nome} ({famiglia.descrizione}) con euristica {tipo_euristica.upper()}...")
    else:
        print(f"\nAnalisi per {famiglia.nome} ({famiglia.descrizione}) con algoritmo {algoritmo.upper()}...")

    #Tempo di inizio
    start_algoritmo = time.time()

    for rifugio in lista_rifugi:
        nodo_end = rifugio.nodo_grafo
        try:
            #scegliamo l'algoritmo di ricerca
            if algoritmo == "A*":
                #Usa la nostra implementazione personalizzata di A* con l'euristica scelta
                percorso_temp = a_star_search_personalizzato(
                    G,
                    source=nodo_start,
                    target=nodo_end,
                    tipo_euristica=tipo_euristica,
                    weight='weight'
                )
            #todo: implementare dijkstra in maniera personalizzata
            elif algoritmo == "dijkstra":
                percorso_temp = nx.dijkstra_path(
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

    tempo_esecuzione = time.time() - start_algoritmo

    print(f"Algoritmo {algoritmo.upper()} completato in {tempo_esecuzione:.4f} secondi")
    return miglior_rifugio, miglior_percorso, min_tempo, tempo_esecuzione
