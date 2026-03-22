import networkx as nx
import time
from algorithms.astar import a_star_search_personalizzato
from algorithms.greedy import greedy_best_first_search
from algorithms.uniform_cost import ricercaInAmpiezzaCU
from graph.graph_utils import get_nearest_node


def scegli_rifugio_migliore(G, famiglia, lista_rifugi, algoritmo="A*", tipo_euristica="euclidea"):
    # Cerca il nodo più vicino alla posizione iniziale della famiglia
    nodo_start = get_nearest_node(G, famiglia.lat, famiglia.lon)
    miglior_rifugio = None
    miglior_percorso = []
    min_tempo = float('inf')
    nodi_esplorati_totali = 0
    tempo_miglior_rifugio = 0.0

    if algoritmo == "A*":
        print(f"\nAnalisi per {famiglia.nome} con A* ed euristica {tipo_euristica.upper()}...")
    else:
        print(f"\nAnalisi per {famiglia.nome} con algoritmo {algoritmo.upper()}...")

    start_algoritmo = time.time()

    for rifugio in lista_rifugi:
        nodo_end = rifugio.nodo_grafo
        try:
            startCronometroSingolo = time.time()

            if algoritmo.upper() == "A*":
                # A* con euristica selezionata
                percorso_temp, nodi = a_star_search_personalizzato(G, nodo_start, nodo_end, tipo_euristica)
            elif algoritmo.upper() == "GREEDY":
                # Greedy Best-First con euristica selezionata
                percorso_temp, nodi = greedy_best_first_search(G, nodo_start, nodo_end, tipo_euristica)
            elif algoritmo.upper() == "CU":
                # Costo Uniforme
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
