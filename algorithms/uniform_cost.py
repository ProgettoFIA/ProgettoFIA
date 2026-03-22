import networkx as nx
import heapq
from typing import Dict, List, Optional, Tuple
from algorithms.astar import ricostruisci_percorso


# RICERCA IN AMPIEZZA CON COSTO UNIFORME (CU)
def ricercaInAmpiezzaCU(G, sorgente, puntoSicuro):
    nodiEsplorati = 0

    # Dizionari
    cameFrom = {sorgente: None}
    gScore = {sorgente: 0}

    # Lista vuota
    frontiera = []
    esplorati = set()

    heapq.heappush(frontiera, (0, sorgente))

    while frontiera:
        # Estrazione della coppia nodo + costo minore
        costoCorrente, nodoCorrente = heapq.heappop(frontiera)

        if nodoCorrente in esplorati:
            continue

        nodiEsplorati += 1

        # Se è il punto sicuro abbiamo finito e ci facciamo restituire il percorso
        if nodoCorrente == puntoSicuro:
            percorso = ricostruisci_percorso(cameFrom, nodoCorrente)
            return percorso, nodiEsplorati

        # Se non è il puntoSicuro, si aggiunge all'insieme dei nodi esplorati
        esplorati.add(nodoCorrente)

        # Espandiamo il nodoCorrente appena inserito nell insieme
        for figlio in G.neighbors(nodoCorrente):
            costoPasso = G[nodoCorrente][figlio]['weight']
            costoFiglio = costoCorrente + costoPasso

            # Se il nodo figlio è stato scoperto per la prima volta oppure è una strada più breve,
            # inseriamo quel nodo nella coda a priorità
            if figlio not in gScore or costoFiglio < gScore[figlio]:
                gScore[figlio] = costoFiglio
                cameFrom[figlio] = nodoCorrente
                heapq.heappush(frontiera, (costoFiglio, figlio))

    # Se non si trova una percorso, eccezione
    raise nx.NetworkXNoPath(f"Nessun percorso trovato tra {sorgente} e {puntoSicuro}")
