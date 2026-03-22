import networkx as nx
import heapq
from typing import Dict, List, Optional, Tuple
from algorithms.heuristics import get_funzione_euristica
from algorithms.astar import ricostruisci_percorso


# GREEDY BEST-FIRST SEARCH
def greedy_best_first_search(G, source, target, tipo_euristica)->Tuple[List[str], int]:
    funzione_dist = get_funzione_euristica(tipo_euristica)

    def euristica(u, v):
        return funzione_dist(G.nodes[u]['pos'], G.nodes[v]['pos'])

    closed_set = set()
    came_from = {}

    open_set = [(euristica(source, target), source)]
    open_set_nodes = {source}
    nodi_esplorati = 0

    while open_set:
        current_h, current = heapq.heappop(open_set)
        open_set_nodes.remove(current)
        nodi_esplorati += 1

        if current == target:
            return ricostruisci_percorso(came_from, current), nodi_esplorati

        closed_set.add(current)

        for neighbor in G.neighbors(current):
            if neighbor in closed_set or neighbor in open_set_nodes:
                continue

            came_from[neighbor] = current
            heapq.heappush(open_set, (euristica(neighbor, target), neighbor))
            open_set_nodes.add(neighbor)

    raise nx.NetworkXNoPath(f"Nessun percorso trovato tra {source} e {target}")
