# main.py
from network import scarica_grafo, get_nearest_node
from classi import NucleoFamiliare, PuntoSicuro
from AI import scegli_rifugio_migliore
from visualization import visualizza_simulazioni_personalizzate

if __name__ == "__main__":
    # Scarica Mappa
    grafo = scarica_grafo()

    if grafo:
        # I vari punti sicuri dove devono andare le persone
        rifugi = [
            PuntoSicuro("HUB Monterusciello", 40.8650, 14.0630),
            PuntoSicuro("Porto di Pozzuoli", 40.8214, 14.1213),
            PuntoSicuro("Stadio Maradona", 40.8279, 14.1930),
            PuntoSicuro("Stadio di Quarto", 40.8800, 14.1300),
            PuntoSicuro("Ippodromo Agnano", 40.8260, 14.1450),
            PuntoSicuro("Aereoporto di Capodichino", 40.9570, 14.4920)
        ]

        print("Indicizzazione Rifugi...")
        for r in rifugi:
            r.nodo_grafo = get_nearest_node(grafo, r.lat, r.lon)

        popolazione = [
            NucleoFamiliare("Fam. Rossi", 40.8320, 14.2260, in_auto=True),
            NucleoFamiliare("Fam. Esposito", 40.8160, 14.1700, in_auto=True, con_fragili=True),
            NucleoFamiliare("Studenti", 40.8500, 14.1500, in_auto=False, con_fragili=False)
            #todo: fare un centinaio di esempi con cui fare i test
        ]

        # Calcola percorsi
        risultati_finali = []
        for fam in popolazione:
            # per l'algoritmo A* (lui valuta tutti i 'rifugi')
            rif_a, path_a, tempo_a, exec_a, nodi_a = scegli_rifugio_migliore(grafo, fam, rifugi, algoritmo="A*",tipo_euristica="euclidea")

            #Forzati i due algoritmi a trovare un percorso solo verso il rifugio scelto da A*
            if rif_a:
                # per l'algoritmo CU
                rif_d, path_d, tempo_d, exec_d, nodo_d = scegli_rifugio_migliore(grafo, fam, [rif_a], algoritmo="CU")

                # per l'algoritmo GREEDY
                rif_g, path_g, tempo_g, exec_g, nodo_g = scegli_rifugio_migliore(grafo, fam, [rif_a],  algoritmo="GREEDY")

                #Confronto risultati
                print(f"A* -> tempo dell'algoritmo: {exec_a:.4f}s")
                print(f"GREEDY -> tempo dell'algoritmo: {exec_g:.4f}s")
                print(f"CU -> tempo dell'algoritmo: {exec_d:.4f}s")


                print(f"✅ ASSEGNATO: {rif_a.nome} in {tempo_a:.0f} minuti.")

                risultati_finali.append((fam, rif_a, path_a, path_d, path_g, tempo_a))

        # Visualizza le mappe
        visualizza_simulazioni_personalizzate(grafo, risultati_finali)