# main.py
from network import scarica_grafo, get_nearest_node
from classi import NucleoFamiliare, PuntoSicuro
from AI import scegli_rifugio_migliore
from visualization import visualizza_simulazioni_personalizzate

if __name__ == "__main__":
    #Scarica Mappa
    grafo = scarica_grafo()

    if grafo:
        #I vari punti sicuri dove devono andare le persone
        rifugi = [
            PuntoSicuro("HUB Monterusciello", 40.8650, 14.0630),
            PuntoSicuro("Porto di Pozzuoli", 40.8214, 14.1213),
            PuntoSicuro("Stadio Maradona", 40.8279, 14.1930),
            PuntoSicuro("Stadio di Quarto", 40.8800, 14.1300),
            PuntoSicuro("Ippodromo Agnano", 40.8260, 14.1450)
        ]

        print("📍 Indicizzazione Rifugi...")
        for r in rifugi:
            r.nodo_grafo = get_nearest_node(grafo, r.lat, r.lon)

        popolazione = [
            NucleoFamiliare("Fam. Rossi", 40.8320, 14.2260, in_auto=True),
            NucleoFamiliare("Fam. Esposito", 40.8160, 14.1700, in_auto=True, con_fragili=True),
            NucleoFamiliare("Studenti", 40.8500, 14.1500, in_auto=False, con_fragili=False)
        ]

        #Calcola percorsi
        risultati_finali = []
        for fam in popolazione:
            best_rif, path, tempo = scegli_rifugio_migliore(grafo, fam, rifugi)
            if best_rif:
                print(f"✅ ASSEGNATO: {best_rif.nome} in {tempo:.0f} minuti.")
                risultati_finali.append((fam, best_rif, path, tempo))

        #Visualizza le mappe
        visualizza_simulazioni_personalizzate(grafo, risultati_finali)