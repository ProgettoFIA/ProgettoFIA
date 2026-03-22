import networkx as nx
import heapq
from typing import Dict, List, Optional, Tuple
from algorithms.heuristics import get_funzione_euristica, EURISTICA_EUCLIDEA


# Ricostruisce il percorso dalla fonte al nodo corrente
def ricostruisci_percorso(came_from: Dict[str, Optional[str]], current: str) -> List[str]:
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        if current is not None:
            total_path.append(current)
    total_path.reverse()
    return total_path


# Implementazione personalizzata dell'algoritmo A* con diverse euristiche che restituisce una lista che contiene il percorso ottimale
def a_star_search_personalizzato(G: nx.Graph,
                                 source: str,
                                 target: str,
                                 tipo_euristica: str = EURISTICA_EUCLIDEA,
                                 weight: str = 'weight') -> Tuple[List[str],int]:

    # Ottieni la funzione euristica selezionata
    funzione_dist = get_funzione_euristica(tipo_euristica)

    # Calcola la distanza tra due nodi usando l'euristica scelta
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

        if current in closed_set:
            continue

        nodi_esplorati += 1

        # Se il nodo corrente è il nodo target, restituisce il percorso
        if current == target:
            return ricostruisci_percorso(came_from, current), nodi_esplorati

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
