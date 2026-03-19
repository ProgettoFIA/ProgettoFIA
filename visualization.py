# visualization.py
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx
import contextily as ctx
import matplotlib.lines as mlines
from utils import converti_latlon_to_mercator


def _converti_percorso(pos, nodi):
    """Converte una lista di nodi in liste separate di coordinate Mercator (X, Y)."""
    coords = [converti_latlon_to_mercator(*pos[n]) for n in nodi]
    return [c[0] for c in coords], [c[1] for c in coords]


def visualizza_simulazioni_personalizzate(G, risultati):
    print("\nGenerazione Mappe Tattiche Personalizzate...")

    pos = nx.get_node_attributes(G, 'pos')

    for famiglia, rifugio, percorso_astar, percorsoCu, percorsoGreedy, tempo in risultati:
        print(f"   -> Generazione mappa per: {famiglia.nome}...")

        # Coordinate Mercator dei tre percorsi
        px_a, py_a = _converti_percorso(pos, percorso_astar)
        px_d, py_d = _converti_percorso(pos, percorsoCu)
        px_g, py_g = _converti_percorso(pos, percorsoGreedy)

        fam_x, fam_y = converti_latlon_to_mercator(famiglia.lat, famiglia.lon)
        rif_x, rif_y = converti_latlon_to_mercator(rifugio.lat,  rifugio.lon)

        # Figure con GridSpec
        # In questo modo la legenda è fuori dall'area cartografica.
        fig = plt.figure(figsize=(12, 11))
        gs  = gridspec.GridSpec(
            2, 1,
            figure=fig,
            height_ratios=[1, 11],
            hspace=0.04
        )
        ax_top = fig.add_subplot(gs[0])   # striscia legenda/titolo
        ax     = fig.add_subplot(gs[1])   # mappa

        ax_top.set_axis_off()

        # Titolo centrato nella striscia superiore
        ax_top.text(
            0.5, 1.15,
            f"PIANO DI FUGA PERSONALIZZATO\nNucleo: {famiglia.nome}",
            transform=ax_top.transAxes,
            ha='center', va='top',
            fontsize=14, fontweight='bold'
        )

        # Handles per la legenda
        astar_line   = mlines.Line2D([], [], color='blue',  linewidth=4,
                                     label='Algoritmo A*')
        cu_line      = mlines.Line2D([], [], color='red',   linewidth=4,
                                     label='Algoritmo CU')
        greedy_line  = mlines.Line2D([], [], color='green', linewidth=4,
                                     label='Algoritmo Greedy')
        start_marker = mlines.Line2D([], [], color='black', marker='o',
                                     linestyle='None', markersize=10,
                                     markerfacecolor='white',
                                     label='Posizione Iniziale')
        dest_marker  = mlines.Line2D([], [], color='black', marker='P',
                                     linestyle='None', markersize=12,
                                     markerfacecolor='white',
                                     label=f'Destinazione: {rifugio.nome}')

        # Legenda orizzontale nella striscia superiore, mai sovrapposta alla mappa
        ax_top.legend(
            handles=[astar_line, cu_line, greedy_line, start_marker, dest_marker],
            loc='lower center',
            bbox_to_anchor=(0.5, -0.05),
            ncol=5,
            frameon=True,
            shadow=True,
            facecolor='white',
            fontsize=9,
            borderpad=0.6,
            columnspacing=1.2
        )

        # Tracciamento percorsi
        ax.plot(px_d, py_d, color='red',   linewidth=6, alpha=0.8, zorder=3)
        ax.plot(px_g, py_g, color='green', linewidth=4, alpha=0.8, zorder=4)
        ax.plot(px_a, py_a, color='blue',  linewidth=4, alpha=0.9, zorder=5)

        # Marker partenza / destinazione
        ax.scatter([fam_x], [fam_y], c='white', s=350, edgecolors='black',
                   linewidth=2, marker='o', zorder=7)
        ax.scatter([rif_x], [rif_y], c='white', s=450, edgecolors='black',
                   linewidth=2, marker='P', zorder=7)

        # Zoom automatico sull'area dei percorsi
        all_x = px_a + px_d + px_g
        all_y = py_a + py_d + py_g
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        pad_x = (max_x - min_x) * 0.15
        pad_y = (max_y - min_y) * 0.15
        ax.set_xlim(min_x - pad_x, max_x + pad_x)
        ax.set_ylim(min_y - pad_y, max_y + pad_y)
        ax.set_aspect('equal')

        # Sfondo OpenStreetMap
        try:
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        except Exception as e:
            print(f"   Errore scaricamento sfondo: {e}")

        ax.set_axis_off()

        plt.savefig(
            f"mappa_{famiglia.nome.replace(' ', '_').replace('/', '-')}.png",
            dpi=150,
            bbox_inches='tight'
        )
        plt.show()
        plt.close(fig)

def visualizza_zona_rossa(cratere_lat=40.8224, cratere_lon=14.4289, raggio_km=4.5):
    """Mostra solo la zona rossa con zoom"""
    fig, ax = plt.subplots(figsize=(10, 10))

    cx, cy = converti_latlon_to_mercator(cratere_lat, cratere_lon)
    from matplotlib.patches import Circle
    cerchio = Circle((cx, cy), raggio_km*1000, color='red', alpha=0.3,
                     label=f'Zona Rossa {raggio_km}km')
    ax.add_patch(cerchio)
    ax.scatter([cx], [cy], c='darkred', s=200, marker='^',
               edgecolors='black', label='Cratere')

    # Zoom sulla zona
    margin = raggio_km * 1500
    ax.set_xlim(cx - raggio_km*1000 - margin, cx + raggio_km*1000 + margin)
    ax.set_ylim(cy - raggio_km*1000 - margin, cy + raggio_km*1000 + margin)

    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13)
    ax.set_axis_off()
    plt.title("Zona Rossa del Vesuvio", fontsize=14, fontweight='bold')
    plt.legend()
    plt.show()