# visualization.py
from cProfile import label

import matplotlib.pyplot as plt
import networkx as nx
import contextily as ctx
import matplotlib.lines as mlines
from utils import converti_latlon_to_mercator


def visualizza_simulazioni_personalizzate(G, risultati):
    print("\nGenerazione Mappe Tattiche Personalizzate...")

    pos = nx.get_node_attributes(G, 'pos')
    colors = ['r', 'b', 'g', 'c', 'm']

    for i, (famiglia, rifugio, percorso_astar, percorsoCu, percorsoGreedy, tempo) in enumerate(risultati):
        colore_famiglia = colors[i % len(colors)]
        fig, ax = plt.subplots(figsize=(10, 10))
        print(f"   -> Generazione mappa per: {famiglia.nome}...")

        #percorso A*
        mercator_astar = []
        for n in percorso_astar:
            lat_n, lon_n = pos[n]
            mx, my = converti_latlon_to_mercator(lat_n, lon_n)
            mercator_astar.append((mx, my))

        #percorso CU
        mercatorCu = []
        for n in percorsoCu:
            lat_n, lon_n = pos[n]
            mx, my = converti_latlon_to_mercator(lat_n, lon_n)
            mercatorCu.append((mx, my))
        px_a = [m[0] for m in mercator_astar]
        py_a = [m[1] for m in mercator_astar]

        px_d = [m[0] for m in mercatorCu]
        py_d=  [m[1] for m in mercatorCu]

        #Percorso Greedy
        mercatorGreedy = []
        for n in percorsoGreedy:
            lat_n, lon_n = pos[n]
            mx, my = converti_latlon_to_mercator(lat_n, lon_n)
            mercatorGreedy.append((mx, my))
        px_g = [m[0] for m in mercatorGreedy]
        py_g=  [m[1] for m in mercatorGreedy]

        #Rappresentazione percorso A*
        ax.plot(px_a, py_a, color="blue", linewidth=4, alpha=0.9,label=f"Percorso A*: {tempo:.0f} min", zorder=5)

        #Rappresentazione percorso CU
        ax.plot(px_d, py_d, color="red", linewidth=6, alpha=0.8, label=f"Percorso CU", zorder=3)

        #Rappresentazione percorso Greedy
        ax.plot(px_g, py_g, color="green", linewidth=4, alpha=0.8, label=f"Percorso Greedy", zorder=4)

        fam_x, fam_y = converti_latlon_to_mercator(famiglia.lat, famiglia.lon)
        rif_x, rif_y = converti_latlon_to_mercator(rifugio.lat, rifugio.lon)

        ax.scatter([fam_x], [fam_y], c=colore_famiglia, s=300, edgecolors='black', marker='o', zorder=6,
                   label="Posizione Iniziale")
        ax.scatter([rif_x], [rif_y], c='white', s=400, marker='P', edgecolors='black', linewidth=2, zorder=6,
                   label=f"DESTINAZIONE: {rifugio.nome}")

        all_x = px_a + px_d + px_g
        all_y = py_a + py_d + py_g

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        margin_x = (max_x - min_x) * 0.2
        margin_y = (max_y - min_y) * 0.2
        ax.set_xlim(min_x - margin_x, max_x + margin_x)
        ax.set_ylim(min_y - margin_y, max_y + margin_y)

        # Mantiene le proporzioni corrette
        ax.set_aspect('equal')

        try:
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        except Exception as e:
            print(f"Errore scaricamento sfondo: {e}")

        ax.set_axis_off()
        plt.title(f"PIANO DI FUGA PERSONALIZZATO\nNucleo: {famiglia.nome} ({famiglia.descrizione})", fontsize=14,fontweight='bold')

        #Legenda per gli algoritmi
        astar_line=mlines.Line2D([],[], color='blue', linewidth=4, label= 'Algoritmo A*')

        cuLine=mlines.Line2D([],[], color='red', linewidth=4, label='Algoritmo CU')

        greedyLine = mlines.Line2D([], [], color='green', linewidth=4, label='Algoritmo Greedy')

        plt.legend(handles=[astar_line, cuLine, greedyLine],
                   loc='upper left',
                   frameon=True,
                   shadow=True,
                   facecolor='white')
        plt.tight_layout()
        plt.show()
