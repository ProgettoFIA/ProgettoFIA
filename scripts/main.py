import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from graph.graph_loader import scarica_grafo, zoneRosse
from graph.graph_utils import get_nearest_node
from core.models import NucleoFamiliare, PuntoSicuro
from algorithms.selector import scegli_rifugio_migliore, esperimento_euristiche_astar, esperimento_greedy_euristiche, esperimentoCU
from visualization.plots import visualizza_simulazioni_personalizzate, visualizza_zona_rossa
import json

if __name__ == "__main__":
    # DIREZIONE 1: Scaricamento della mappa stradale
    grafo = scarica_grafo()

    if grafo:
        # DIREZIONE 2: Attivazione zona rossa per escludere aree pericolose
        grafo = zoneRosse(grafo, crater_lat=40.8224, crater_lon=14.4289, raggio_km=4.5)

        print("Indicizzazione Rifugi...")

        # VERSANTE PRINCIPALE: Definizione dei punti sicuri (rifugi)
        rifugi = [
            PuntoSicuro("HUB Monterusciello (Pozzuoli)", 40.8650, 14.0630),
            PuntoSicuro("Porto Turistico (Bacoli)", 40.7950, 14.0800),

            PuntoSicuro("Stadio Romeo Menti (Castellammare)", 40.7050, 14.4850),
            PuntoSicuro("Campo Sportivo (Sorrento)", 40.6280, 14.3820)
        ]

        for r in rifugi:
            r.nodo_grafo = get_nearest_node(grafo, r.lat, r.lon)

        # VERSANTE SECONDARIO: Definizione della popolazione (nuclei familiari) a rischio
        popolazione = [
            NucleoFamiliare("Fam. Esposito (Portici)", 40.8160, 14.3400, con_fragili=False),
            NucleoFamiliare("Fam. Romano (Ercolano)", 40.8060, 14.3490, con_fragili=True),
            NucleoFamiliare("Fam. De Luca (Torre del Greco)", 40.7850, 14.3720, con_fragili=False),
            NucleoFamiliare("Fam. Greco (Torre Annunziata)", 40.7550, 14.4440, con_fragili=False),

            NucleoFamiliare("Fam. Conti (Pompei)", 40.7500, 14.5000, con_fragili=False),
            NucleoFamiliare("Fam. Fontana (Boscoreale)", 40.7750, 14.4750, con_fragili=True),
            NucleoFamiliare("Fam. Marino (Boscotrecase)", 40.7760, 14.4610, con_fragili=False),

            NucleoFamiliare("Fam. Lombardi (Terzigno)", 40.8030, 14.5020, con_fragili=False),
            NucleoFamiliare("Fam. Moretti (San Giuseppe Ves.)", 40.8300, 14.5030, con_fragili=True),
            NucleoFamiliare("Fam. Barbieri (Ottaviano)", 40.8500, 14.4780, con_fragili=False),

            NucleoFamiliare("Fam. Ferrara (Somma Vesuviana)", 40.8710, 14.4370, con_fragili=True),
            NucleoFamiliare("Fam. Rinaldi (Sant'Anastasia)", 40.8650, 14.3980, con_fragili=True),

            NucleoFamiliare("Fam. Leone (Cercola)", 40.8550, 14.3560, con_fragili=False),
            NucleoFamiliare("Fam. Gallo (San Giorgio a C.)", 40.8280, 14.3350, con_fragili=False),
            NucleoFamiliare("Fam. Santoro (San Sebastiano)", 40.8400, 14.3380, con_fragili=True),
        ]

        popolazione.sort(key = lambda x: x.con_fragili, reverse=True)

        # Elaborazione e assegnazione di ogni famiglia al rifugio migliore con confronto algoritmico
        risultati_finali = []
        for fam in popolazione:

            rifugiDisponibili = [r for r in rifugi if not r.isPieno()]

            if not rifugiDisponibili:
                print(f"Nessun rifugio disponibile per {fam.nome}. Tutti i rifugi sono pieni.")
                continue

            rif_a, path_a, tempo_a, exec_a_totale, nodi_a, exec_a_migliore = scegli_rifugio_migliore(grafo, fam, rifugiDisponibili, algoritmo="A*",tipo_euristica="euclidea")

            rif_d, path_d, tempo_d, exec_d_totale, nodo_d,exec_d_migliore = scegli_rifugio_migliore(grafo, fam, rifugiDisponibili, algoritmo="CU")

            rif_g, path_g, tempo_g, exec_g_totale, nodo_g,exec_g_migliore = scegli_rifugio_migliore(grafo, fam, rifugiDisponibili, algoritmo="GREEDY")

            if rif_a:

                rif_a.aggiungiFamiglia()

                print("\n")
                print(f"A* -> tempo dell'algoritmo: {exec_a_migliore:.4f}s")
                print(f"GREEDY -> tempo dell'algoritmo: {exec_g_migliore:.4f}s")
                print(f"CU -> tempo dell'algoritmo: {exec_d_migliore:.4f}s")

                posti_rimanenti = rif_a.capacita_max - rif_a.famiglie_assegnate
                print(f"✅ ASSEGNATO: {rif_a.nome} in {tempo_a:.0f} minuti.")
                print(f"⚠️ Posti rimanenti in {rif_a.nome} : {posti_rimanenti}")

                for r in rifugi:
                    print("-"*50)
                    print(f"   - {r.nome}: {r.capacita_max - r.famiglie_assegnate} posti rimanenti")
                    print("-" * 50)

                risultati_finali.append((fam, rif_a, path_a, path_d, path_g, tempo_a))

        # BENCHMARK A*
        euristiche = ["euclidea", "manhattan", "chebyshev"]
        tempi_percorrenza_astar, tempi_esecuzione_astar = esperimento_euristiche_astar(grafo, popolazione, rifugi, euristiche)

        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA A*")
        print("-"*70)
        print(f"{'EURISTICA':15} | {'MEDIA PERCORRENZA (min)':25} | {'MEDIA ESECUZIONE (s)':25}")
        print("-"*70)
        medie_percorrenza_astar = {}
        medie_esecuzione_astar = {}
        for eur in euristiche:
            media_perc = sum(tempi_percorrenza_astar[eur]) / len(tempi_percorrenza_astar[eur])
            media_exec = sum(tempi_esecuzione_astar[eur]) / len(tempi_esecuzione_astar[eur])
            medie_percorrenza_astar[eur] = media_perc
            medie_esecuzione_astar[eur] = media_exec
            print(f"{eur.upper():15} | {media_perc:23.2f} min | {media_exec:23.4f}s")

        migliore_perc_astar = min(medie_percorrenza_astar, key=medie_percorrenza_astar.get)
        migliore_exec_astar = min(medie_esecuzione_astar, key=medie_esecuzione_astar.get)
        print(f"\nMigliore per tempo di percorrenza: {migliore_perc_astar.upper()} ({medie_percorrenza_astar[migliore_perc_astar]:.2f} min)")
        print(f"Migliore per velocità dell'algoritmo: {migliore_exec_astar.upper()} ({medie_esecuzione_astar[migliore_exec_astar]:.4f}s)")

        # BENCHMARK GREEDY
        tempi_percorrenza_greedy, tempi_esecuzione_greedy = esperimento_greedy_euristiche(grafo, popolazione, rifugi, euristiche)
        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA GREEDY")
        print("-"*70)
        print(f"{'EURISTICA':15} | {'MEDIA PERCORRENZA (min)':25} | {'MEDIA ESECUZIONE (s)':25}")
        print("-"*70)
        medie_percorrenza_greedy = {}
        medie_esecuzione_greedy = {}
        for eur in euristiche:
            media_perc = sum(tempi_percorrenza_greedy[eur]) / len(tempi_percorrenza_greedy[eur])
            media_exec = sum(tempi_esecuzione_greedy[eur]) / len(tempi_esecuzione_greedy[eur])
            medie_percorrenza_greedy[eur] = media_perc
            medie_esecuzione_greedy[eur] = media_exec
            print(f"{eur.upper():15} | {media_perc:23.2f} min | {media_exec:23.4f}s")

        migliore_perc_greedy = min(medie_percorrenza_greedy, key=medie_percorrenza_greedy.get)
        migliore_exec_greedy = min(medie_esecuzione_greedy, key=medie_esecuzione_greedy.get)

        print("-"*70)
        print(f"Migliore per tempo percorrenza: {migliore_perc_greedy.upper()} ({medie_percorrenza_greedy[migliore_perc_greedy]:.2f} min)")
        print(f"Migliore per velocità dell'algoritmo: {migliore_exec_greedy.upper()} ({medie_esecuzione_greedy[migliore_exec_greedy]:.4f}s)")

        # BENCHMARK CU
        tempiPercorrenzaCU, tempiEsecuzioneCu = esperimentoCU(grafo, popolazione, rifugi)
        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA CU")
        print("-"*70)
        print(f"{'ALGORITMO':15} | {'MEDIA PERCORRENZA (min)':25} | {'MEDIA ESECUZIONE (s)':25}")
        print("-"*70)

        mediaPercorrenzaCU = sum(tempiPercorrenzaCU) / len(tempiPercorrenzaCU)
        mediaEsecuzioneCU = sum(tempiEsecuzioneCu) / len(tempiEsecuzioneCu)

        print(f"{'CU':15} | {mediaPercorrenzaCU:23.2f} min | {mediaEsecuzioneCU:23.4f}s")

        # Salva i risultati del benchmark in JSON per la visualizzazione
        benchmark_results = {
            "astar": {
                "medie_percorrenza": medie_percorrenza_astar,
                "medie_esecuzione": medie_esecuzione_astar,
                "migliore_percorrenza": migliore_perc_astar,
                "migliore_esecuzione": migliore_exec_astar
            },
            "greedy": {
                "medie_percorrenza": medie_percorrenza_greedy,
                "medie_esecuzione": medie_esecuzione_greedy,
                "migliore_percorrenza": migliore_perc_greedy,
                "migliore_esecuzione": migliore_exec_greedy
            },
            "cu": {
                "media_percorrenza": mediaPercorrenzaCU,
                "media_esecuzione": mediaEsecuzioneCU
            }
        }

        with open("benchmark_results.json", "w") as f:
            json.dump(benchmark_results, f, indent=4)
        print("\nRisultati benchmark salvati in benchmark_results.json")

        visualizza_simulazioni_personalizzate(grafo, risultati_finali)

        visualizza_zona_rossa()
