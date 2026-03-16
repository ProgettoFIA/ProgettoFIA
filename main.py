# main.py
from network import scarica_grafo, get_nearest_node, zoneRosse
from classi import NucleoFamiliare, PuntoSicuro
from AI import scegli_rifugio_migliore, esperimento_euristiche_astar, esperimento_greedy_euristiche, esperimentoCU
from visualization import visualizza_simulazioni_personalizzate
import time

if __name__ == "__main__":
    # Scarica Mappa
    grafo = scarica_grafo()

    if grafo:
        # Applica la zona rossa al grafo prima di indicizzare i rifugi
        grafo = zoneRosse(grafo, crater_lat=40.8224, crater_lon=14.4289, raggio_km=4.5)

        # I vari punti sicuri dove devono andare le persone
        print("Indicizzazione Rifugi...")

        #TODO ancora non mi convincono a pieno i rifugi/popolazione. Da migliorare

        rifugi = [
            # DIREZIONE OVEST (Sinistra di Napoli)
            PuntoSicuro("HUB Monterusciello (Pozzuoli)", 40.8650, 14.0630),
            PuntoSicuro("Porto Turistico (Bacoli)", 40.7950, 14.0800),

            # DIREZIONE SUD (Penisola Sorrentina)
            PuntoSicuro("Stadio Romeo Menti (Castellammare)", 40.7050, 14.4850),
            PuntoSicuro("Campo Sportivo (Sorrento)", 40.6280, 14.3820)
        ]

        for r in rifugi:
            r.nodo_grafo = get_nearest_node(grafo, r.lat, r.lon)

        popolazione = [
            # Versante Costiero (Sud-Ovest del Vesuvio)
            NucleoFamiliare("Fam. Esposito (Portici)", 40.8160, 14.3400, con_fragili=False),
            NucleoFamiliare("Fam. Romano (Ercolano)", 40.8060, 14.3490, con_fragili=True),
            NucleoFamiliare("Fam. De Luca (Torre del Greco)", 40.7850, 14.3720, con_fragili=False),
            NucleoFamiliare("Fam. Greco (Torre Annunziata)", 40.7550, 14.4440, con_fragili=False),

            # Versante Sud-Est (Zona Pompei/Scafati)
            NucleoFamiliare("Fam. Conti (Pompei)", 40.7500, 14.5000, con_fragili=False),
            NucleoFamiliare("Fam. Fontana (Boscoreale)", 40.7750, 14.4750, con_fragili=True),
            NucleoFamiliare("Fam. Marino (Boscotrecase)", 40.7760, 14.4610, con_fragili=False),

            # Versante Est / Entroterra
            NucleoFamiliare("Fam. Lombardi (Terzigno)", 40.8030, 14.5020, con_fragili=False),
            NucleoFamiliare("Fam. Moretti (San Giuseppe Ves.)", 40.8300, 14.5030, con_fragili=True),
            NucleoFamiliare("Fam. Barbieri (Ottaviano)", 40.8500, 14.4780, con_fragili=False),

            # Versante Nord (Alle spalle del Somma)
            NucleoFamiliare("Fam. Ferrara (Somma Vesuviana)", 40.8710, 14.4370, con_fragili=True),
            NucleoFamiliare("Fam. Rinaldi (Sant'Anastasia)", 40.8650, 14.3980, con_fragili=True),

            # Versante Nord-Ovest (Tra Vesuvio e Napoli)
            NucleoFamiliare("Fam. Leone (Cercola)", 40.8550, 14.3560, con_fragili=False),
            NucleoFamiliare("Fam. Gallo (San Giorgio a C.)", 40.8280, 14.3350, con_fragili=False),
            NucleoFamiliare("Fam. Santoro (San Sebastiano)", 40.8400, 14.3380, con_fragili=True),
        ]

        # Ordina la popolazione in modo che le famiglie con soggetti fragili vengano assegnate per prime ai rifugi
        # aumentando così le probabilità di assegnarle a quelli più vicini e sicuri
        popolazione.sort(key = lambda x: x.con_fragili, reverse=True)
        """
        # BENCHMARK A*
        euristiche= ["euclidea", "manhattan", "chebyshev"]
        tempi_percorrenza_astar, tempi_esecuzione_astar= esperimento_euristiche_astar(grafo, popolazione, rifugi, euristiche)

        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA A*")
        print("-"*70)
        print(f"{'EURISTICA':15} | {'MEDIA PERCORRENZA (min)':25} | {'MEDIA ESECUZIONE (s)':25}")
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

        # BENCHMARK GREEDY
        tempi_percorrenza_greedy, tempi_esecuzione_greedy = esperimento_greedy_euristiche(grafo, popolazione, rifugi, euristiche)
        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA GREEDY")
        print("-"*70)
        print(f"{'EURISTICA':15} | {'MEDIA PERCORRENZA (min)':25} | {'MEDIA ESECUZIONE (s)':25}")
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
        


        # BENCHMARK CU
        tempiPercorrenzaCU, tempiEsecuzioneCu = esperimentoCU(grafo, popolazione, rifugi)
        print("\n" + "-"*70)
        print("TABELLA RIASSUNTIVA CU")
        print("-"*70)
        print(f"{'ALGORITMO':15} | {'MEDIA PERCORRENZA (min)':25} | {'MEDIA ESECUZIONE (s)':25}")
        print("-"*70)

        mediaPercorrenzaCU = sum(tempiPercorrenzaCU) / len(tempiPercorrenzaCU)
        mediaEsecuzioneCU = sum(tempiEsecuzioneCu) / len(tempiEsecuzioneCu)

        print(f"{'CU':15} | {mediaPercorrenzaCU:23.2f} min | {mediaEsecuzioneCU:23.4f} s")
        """
        # Calcola percorsi
        risultati_finali = []
        for fam in popolazione:

            # Lista dei rifugi ancora disponibili
            rifugiDisponibili = [r for r in rifugi if not r.isPieno()]

            # Se non ci sono rifugi disponibili
            # (teoricamente non dovrebbe accadere con i dati attuali, ma è una buona pratica gestire questo caso)
            if not rifugiDisponibili:
                print(f"Nessun rifugio disponibile per {fam.nome}. Tutti i rifugi sono pieni.")
                continue

            # per l'algoritmo A* (lui valuta tutti i 'rifugi')
            rif_a, path_a, tempo_a, exec_a_totale, nodi_a, exec_a_migliore = scegli_rifugio_migliore(grafo, fam, rifugiDisponibili, algoritmo="A*",tipo_euristica="euclidea")

            #Forzati i due algoritmi a trovare un percorso solo verso il rifugio scelto da A*
            if rif_a:

                # Aggiungiamo la famiglia al rifugio scelto da A*
                rif_a.aggiungiFamiglia()

                # per l'algoritmo CU
                rif_d, path_d, tempo_d, exec_d_totale, nodo_d,exec_d_migliore = scegli_rifugio_migliore(grafo, fam, [rif_a], algoritmo="CU")

                # per l'algoritmo GREEDY
                rif_g, path_g, tempo_g, exec_g_totale, nodo_g,exec_g_migliore = scegli_rifugio_migliore(grafo, fam, [rif_a],  algoritmo="GREEDY")

                #Confronto risultati
                print("\n")
                print(f"A* -> tempo dell'algoritmo: {exec_a_migliore:.4f}s")
                print(f"GREEDY -> tempo dell'algoritmo: {exec_g_migliore:.4f}s")
                print(f"CU -> tempo dell'algoritmo: {exec_d_migliore:.4f}s")

                posti_rimanenti = rif_a.capacita_max - rif_a.famiglie_assegnate
                print(f"✅ ASSEGNATO: {rif_a.nome} in {tempo_a:.0f} minuti.")
                print(f"⚠️ Posti rimanenti in {rif_a.nome} : {posti_rimanenti}")

                # Tabella con i posti rimanenti in ogni rifugio dopo ogni assegnazione
                for r in rifugi:
                    print("-"*50)
                    print(f"   - {r.nome}: {r.capacita_max - r.famiglie_assegnate} posti rimanenti")
                    print("-" * 50)

                risultati_finali.append((fam, rif_a, path_a, path_d, path_g, tempo_a))

        # Visualizza le mappe
        visualizza_simulazioni_personalizzate(grafo, risultati_finali)
