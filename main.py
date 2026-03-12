# main.py
from network import scarica_grafo, get_nearest_node
from classi import NucleoFamiliare, PuntoSicuro
from AI import scegli_rifugio_migliore, esperimento_euristiche_astar, esperimento_greedy_euristiche
from visualization import visualizza_simulazioni_personalizzate
import time

if __name__ == "__main__":
    # Scarica Mappa
    grafo = scarica_grafo()

    if grafo:
        # I vari punti sicuri dove devono andare le persone
        print("Indicizzazione Rifugi...")
        rifugi = [
            PuntoSicuro("Caserta", 41.0742, 14.3327),
            PuntoSicuro("Benevento", 41.1298, 14.7826),
            PuntoSicuro("Avellino", 40.9142, 14.7888),
            PuntoSicuro("Salerno", 40.6824, 14.7681),
        ]
        for r in rifugi:
            r.nodo_grafo = get_nearest_node(grafo, r.lat, r.lon)

        popolazione = [
            NucleoFamiliare("Fam. Esposito", 40.7870, 14.3680, in_auto=True),
            NucleoFamiliare("Fam. Romano", 40.8050, 14.3500, in_auto=False, con_fragili=True),
            NucleoFamiliare("Fam. De Luca", 40.8100, 14.3400, in_auto=True),
            NucleoFamiliare("Fam. Conti", 40.8436, 14.3699, in_auto=True, con_fragili=False),
            NucleoFamiliare("Fam. Fontana", 40.8450, 14.3750, in_auto=False, con_fragili=True),
            NucleoFamiliare("Fam. Marino", 40.7750, 14.4620, in_auto=True),
            NucleoFamiliare("Fam. Greco", 40.7700, 14.4380, in_auto=False, con_fragili=False),
            NucleoFamiliare("Fam. Lombardi", 40.8400, 14.4800, in_auto=True),
            NucleoFamiliare("Fam. Moretti", 40.8700, 14.4400, in_auto=True, con_fragili=True),
            NucleoFamiliare("Fam. Barbieri", 40.8600, 14.4000, in_auto=False, con_fragili=False),
            NucleoFamiliare("Fam. Ferrara", 40.7450, 14.5000, in_auto=True),
            NucleoFamiliare("Fam. Rinaldi", 40.7570, 14.4520, in_auto=False, con_fragili=True),
            NucleoFamiliare("Fam. Leone", 40.7750, 14.4750, in_auto=True),
            NucleoFamiliare("Fam. Gallo", 40.8000, 14.5000, in_auto=False, con_fragili=False),
            NucleoFamiliare("Fam. Santoro", 40.8300, 14.5200, in_auto=True),
        ]

        # ESPERIMENTO EURISTICHE A*
        euristiche= ["euclidea", "manhattan", "chebyshev"]
        tempi_percorrenza_astar, tempi_esecuzione_astar= esperimento_euristiche_astar(grafo, popolazione, rifugi, euristiche)

        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA A*")
        print("-"*70)
        print(f"{'EURISTICA':15} | {'TEMPO PERCORRENZA (min)':25} | {'TEMPO ESECUZIONE (s)':25}")
        print("-"*70)
        medie_percorrenza_astar= {}
        medie_esecuzione_astar={}
        for eur in euristiche:
            media_perc= sum(tempi_percorrenza_astar[eur])/ len(tempi_percorrenza_astar[eur])
            media_exec= sum(tempi_esecuzione_astar[eur]) / len (tempi_esecuzione_astar[eur])
            medie_percorrenza_astar[eur]=media_perc
            medie_esecuzione_astar[eur] = media_exec
            print(f"{eur.upper():15} | {media_perc:23.2f} min | {media_exec:23.4f}s ")

        migliore_perc_astar = min(medie_percorrenza_astar, key=medie_percorrenza_astar.get)
        migliore_exec_astar = min(medie_esecuzione_astar, key=medie_esecuzione_astar.get)
        print(f"\nMigliore per tempo di percorrenza: {migliore_perc_astar.upper()}({medie_percorrenza_astar[migliore_perc_astar]:.2f} min)")
        print(f"Migliore per velocità dell'algoritmo: {migliore_exec_astar.upper()}({medie_esecuzione_astar[migliore_exec_astar]:.4f} s)")

        #ESPERIMENTO EURISTICHE GREEDY
        tempi_percorrenza_greedy, tempi_esecuzione_greedy = esperimento_greedy_euristiche(grafo, popolazione, rifugi, euristiche)
        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA GREEDY")
        print("-"*70)
        print(f"{'EURISTICA':15} | {'TEMPO PERCORRENZA (min)':25} | {'TEMPO ESECUZIONE (s)':25}")
        print("-"*70)
        medie_percorrenza_greedy={}
        medie_esecuzione_greedy={}
        for eur in euristiche:
            media_perc=sum(tempi_percorrenza_greedy[eur]) / len (tempi_percorrenza_greedy[eur])
            media_exec =sum(tempi_esecuzione_greedy[eur]) / len (tempi_esecuzione_greedy[eur])

            medie_percorrenza_greedy[eur] = media_perc
            medie_esecuzione_greedy[eur] = media_exec
            print(f"{eur.upper():10}| {media_perc:23.2f} min  | {media_exec:23.4f} s")

        migliore_perc_greedy= min(medie_percorrenza_greedy, key=medie_percorrenza_greedy.get)
        migliore_exec_greedy = min(medie_esecuzione_greedy, key=medie_esecuzione_greedy.get)
        print("-"*70)
        print(f"Miglior per tempo percorrenza: {migliore_perc_greedy.upper()} ({medie_percorrenza_greedy[migliore_perc_greedy]:.2f} min)")
        print(f"Migliore per velocità dell'algoritmo: {migliore_exec_greedy.upper()} ({medie_esecuzione_greedy[migliore_exec_greedy]:.4f} s)")
        # Calcola percorsi
        risultati_finali = []
        for fam in popolazione:
            #per l'algoritmo A*
            rif_a, path_a, tempo_a, exec_a, nodi_a = scegli_rifugio_migliore(grafo, fam, rifugi, algoritmo="A*",tipo_euristica="euclidea")
            #per l'algoritmo CU
            rif_d,path_d,tempo_d,exec_d, nodo_d =scegli_rifugio_migliore(grafo,fam,rifugi,algoritmo="CU")
            #per l'algortmo GREEDY
            rif_g, path_g, tempo_g, exec_g, nodo_g = scegli_rifugio_migliore(grafo, fam, rifugi, algoritmo="GREEDY")
            #facciamo un confronto tra i due
            print(f"A* -> tempo dell'algoritmo: {exec_a:.4f}s")
            print(f"GREEDY -> tempo dell'algoritmo: {exec_g:.4f}s")
            print(f"CU -> tempo dell'algoritmo: {exec_d:.4f}s")

            if rif_a:
                print(f"✅ ASSEGNATO: {rif_a.nome} in {tempo_a:.0f} minuti.")
                risultati_finali.append((fam, rif_a, path_a, path_d, tempo_a))

        # Visualizza le mappe
        visualizza_simulazioni_personalizzate(grafo, risultati_finali)
