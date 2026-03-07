# visualization.py
import matplotlib.pyplot as plt
import networkx as nx
import contextily as ctx
from utils import converti_latlon_to_mercator


def visualizza_simulazioni_personalizzate(G, risultati):
    print("\n🎨 Generazione Mappe Tattiche Personalizzate...")

    pos = nx.get_node_attributes(G, 'pos')
    colors = ['r', 'b', 'g', 'c', 'm']

    for i, (famiglia, rifugio, percorso, tempo) in enumerate(risultati):
        colore_famiglia = colors[i % len(colors)]
        fig, ax = plt.subplots(figsize=(10, 10))
        print(f"   -> Generazione mappa per: {famiglia.nome}...")

        mercator_path = []
        for n in percorso:
            lat_n, lon_n = pos[n]
            mx, my = converti_latlon_to_mercator(lat_n, lon_n)
            mercator_path.append((mx, my))

        px = [m[0] for m in mercator_path]
        py = [m[1] for m in mercator_path]

        ax.plot(px, py, color=colore_famiglia, linewidth=5, alpha=0.8,
                label=f"Percorso: {tempo:.0f} min", zorder=5)

        fam_x, fam_y = converti_latlon_to_mercator(famiglia.lat, famiglia.lon)
        rif_x, rif_y = converti_latlon_to_mercator(rifugio.lat, rifugio.lon)

        ax.scatter([fam_x], [fam_y], c=colore_famiglia, s=300, edgecolors='black', marker='o', zorder=6,
                   label="Posizione Iniziale")
        ax.scatter([rif_x], [rif_y], c='green', s=400, marker='P', edgecolors='black', linewidth=2, zorder=6,
                   label=f"DESTINAZIONE: {rifugio.nome}")

        min_x, max_x = min(px), max(px)
        min_y, max_y = min(py), max(py)
        margin_x = (max_x - min_x) * 0.2
        margin_y = (max_y - min_y) * 0.2
        ax.set_xlim(min_x - margin_x, max_x + margin_x)
        ax.set_ylim(min_y - margin_y, max_y + margin_y)

        # Mantiene le proporzioni corrette
        ax.set_aspect('equal')

        try:
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        except Exception as e:
            print(f"⚠️ Errore scaricamento sfondo: {e}")

        ax.set_axis_off()
        plt.title(f"PIANO DI FUGA PERSONALIZZATO\nNucleo: {famiglia.nome} ({famiglia.descrizione})", fontsize=14,
                  fontweight='bold')
        plt.legend(loc='upper left', frameon=True, shadow=True, facecolor='white')
        plt.tight_layout()
        plt.show()
