import networkx as nx
from network import get_nearest_node
import time
import heapq
import math
from typing import Dict, List, Optional, Tuple, Callable

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


# Ricostruisce il percorso dalla fonte al nodo corrente
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
    nodi_esplorati_totali = 0  # Contatore metriche
    tempo_miglior_rifugio = 0.0

    # Scelta dell'euristica
    if algoritmo == "A*":
        print(f"\nAnalisi per {famiglia.nome} con A* ed euristica {tipo_euristica.upper()}...")
    else:
        print(f"\nAnalisi per {famiglia.nome} con algoritmo {algoritmo.upper()}...")

    start_algoritmo = time.time()

    for rifugio in lista_rifugi:
        nodo_end = rifugio.nodo_grafo
        try:
            # Tempo di esecuzione per ogni rifugio (da parte di A*)
            startCronometroSingolo = time.time()

            # SELETTORE ALGORITMI
            if algoritmo.upper() == "A*":
                percorso_temp, nodi = a_star_search_personalizzato(G, nodo_start, nodo_end, tipo_euristica)
            elif algoritmo.upper() == "GREEDY":
                percorso_temp, nodi = greedy_best_first_search(G, nodo_start, nodo_end, tipo_euristica)
            elif algoritmo.upper() == "CU":
                percorso_temp, nodi = ricercaInAmpiezzaCU(G, nodo_start, nodo_end)
            else:
                raise ValueError(f"Algoritmo {algoritmo} non supportato")

            tempo_singolo = time.time() - startCronometroSingolo

            nodi_esplorati_totali += nodi
            path_len = nx.path_weight(G, percorso_temp, weight='weight')
            tempo_minuti = (path_len / famiglia.speed_ms) / 60

            print(
                f"   -> Verso {rifugio.nome}: {path_len / 1000:.1f} km ({tempo_minuti:.0f} min) - Nodi esplorati: {nodi} | Calcolo: {tempo_singolo:.4f}s")

            if tempo_minuti < min_tempo:
                min_tempo = tempo_minuti
                miglior_rifugio = rifugio
                miglior_percorso = percorso_temp
                tempo_miglior_rifugio = tempo_singolo

        except nx.NetworkXNoPath:
            print(f"   -> {rifugio.nome}: NON RAGGIUNGIBILE")

    tempo_esecuzione = time.time() - start_algoritmo
    if algoritmo == "A*":
        print(f"Miglior rifugio trovato in {tempo_miglior_rifugio:.4f} sec: {miglior_rifugio.nome if miglior_rifugio else 'Nessuno'} con tempo di percorrenza stimato di {min_tempo:.0f} min.")

    print(f"Completato in {tempo_esecuzione:.4f} sec. Nodi esplorati totali: {nodi_esplorati_totali}")

    return miglior_rifugio, miglior_percorso, min_tempo, tempo_esecuzione, nodi_esplorati_totali, tempo_miglior_rifugio

def esperimento_euristiche_astar(G,famiglie,rifugi,euristiche):
    tempi_percorrenza={eur:[]for eur in euristiche}
    tempi_esecuzione={eur: [] for eur in euristiche}
    for eur in euristiche:
        print(f"\n===== Test euristica: {eur.upper()} =====")
        for fam in famiglie:
            nodo_start= get_nearest_node(G,fam.lat, fam.lon)
            for rif in rifugi:
                nodo_end=rif.nodo_grafo
                if nodo_start==nodo_end:
                    print(f"{fam.nome} -> {rif.nome}: STESSO NODO (escluso dalle medie)")

                    continue
                try:
                    start_time=time.time()
                    path, nodi= a_star_search_personalizzato(
                    G,
                    nodo_start,
                    nodo_end,
                    eur
                    )
                    exec_time=time.time() - start_time
                    path_len=nx.path_weight(G,path,weight='weight')
                    tempo_minuti=(path_len / fam.speed_ms)/60

                    if tempo_minuti<0.01:
                        print(f"{fam.nome} -> {rif.nome}: TEMPO TROPPO BASSO (escluso)")
                        continue

                    tempi_percorrenza[eur].append(tempo_minuti)
                    tempi_esecuzione[eur].append(exec_time)

                    print(f"{fam.nome} -> {rif.nome}: {tempo_minuti:.2f} min (algoritmo: {exec_time:.4f}s)")
                except nx.NetworkXNoPath:
                    print(f"{fam.nome} -> {rif.nome}: NON RAGGIUNGIBILE")
    for eur in euristiche:
        print(f"   [DEBUG] {eur}: {len(tempi_percorrenza[eur])} percorsi validi")
    return tempi_percorrenza, tempi_esecuzione


def esperimento_greedy_euristiche(G,famiglie,rifugi,euristiche):
    tempi_percorrenza = {eur: [] for eur in euristiche}
    tempi_esecuzione = {eur: [] for eur in euristiche}

    for eur in euristiche:
        print(f"\n===== [GREEDY] Test euristica: {eur.upper()} =====")
        for fam in famiglie:
            nodo_start=get_nearest_node(G,fam.lat,fam.lon)
            for rif in rifugi:
                nodo_end=rif.nodo_grafo
                if nodo_start == nodo_end:
                    print(f"   {fam.nome} -> {rif.nome}: STESSO NODO (escluso)")
                    continue
                try:
                    start_time=time.time()
                    path,nodi=greedy_best_first_search(G,nodo_start,nodo_end,eur)
                    exec_time=time.time() - start_time
                    path_len=nx.path_weight(G,path,weight='weight')
                    tempo_minuti=(path_len/fam.speed_ms)/60
                    if tempo_minuti < 0.01:
                        print(f"   {fam.nome} -> {rif.nome}: TEMPO TROPPO BASSO (escluso)")
                        continue
                    tempi_percorrenza[eur].append(tempo_minuti)
                    tempi_esecuzione[eur].append(exec_time)
                    print(f"   {fam.nome} -> {rif.nome}: {tempo_minuti:.2f} min")
                except nx.NetworkXNoPath:
                    print(f"   {fam.nome} -> {rif.nome}: NON RAGGIUNGIBILE")
    for eur in euristiche:
        print(f"   [DEBUG] {eur}: {len(tempi_percorrenza[eur])} percorsi validi")
    return tempi_percorrenza, tempi_esecuzione

# Copiato da esperimento_euristiche_astar e a esperimento_greedy_euristiche e adattato per l algoritmo CU,
# rimuovendo tutti i riferimenti alle euristiche
def esperimentoCU(G,famiglie,rifugi):

    tempi_percorrenza = []
    tempi_esecuzione = []

    print(f"\n===== Test Algoritmo: COSTO UNIFORME (CU) =====")
    for fam in famiglie:
        nodo_start = get_nearest_node(G, fam.lat, fam.lon)
        for rif in rifugi:
            nodo_end = rif.nodo_grafo
            if nodo_start == nodo_end:
                print(f"   {fam.nome} -> {rif.nome}: STESSO NODO (escluso)")
                continue
            try:
                start_time = time.time()

                path, nodi = ricercaInAmpiezzaCU(G, nodo_start, nodo_end)

                exec_time = time.time() - start_time
                path_len = nx.path_weight(G, path, weight='weight')
                tempo_minuti = (path_len / fam.speed_ms) / 60

                if tempo_minuti < 0.01:
                     print(f"   {fam.nome} -> {rif.nome}: TEMPO TROPPO BASSO (escluso)")
                     continue

                tempi_percorrenza.append(tempo_minuti)
                tempi_esecuzione.append(exec_time)

                print(f"   {fam.nome} -> {rif.nome}: {tempo_minuti:.2f} min")
            except nx.NetworkXNoPath:
                print(f"   {fam.nome} -> {rif.nome}: NON RAGGIUNGIBILE")

    print(f"   [DEBUG] CU: {len(tempi_percorrenza)} percorsi validi")
    return tempi_percorrenza, tempi_esecuzione


