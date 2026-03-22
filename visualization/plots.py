import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import networkx as nx
import contextily as ctx
import matplotlib.lines as mlines
from utils.coordinates import converti_latlon_to_mercator


def _converti_percorso(pos, nodi):
    # Converte il percorso da coordinate geografiche a coordinate Mercator per la visualizzazione
    coords = [converti_latlon_to_mercator(*pos[n]) for n in nodi]
    return [c[0] for c in coords], [c[1] for c in coords]


def visualizza_simulazioni_personalizzate(G, risultati):
    # Generazione di mappe tattiche personalizzate per ogni famiglia, 
    # mostrando i 3 algoritmi a confronto (A*, Greedy, Costo Uniforme)
    print("\nGenerazione Mappe Tattiche Personalizzate...")

    pos = nx.get_node_attributes(G, 'pos')

    for famiglia, rifugio, percorso_astar, percorsoCu, percorsoGreedy, tempo in risultati:
        print(f"   -> Generazione mappa per: {famiglia.nome}...")

        px_a, py_a = _converti_percorso(pos, percorso_astar)
        px_d, py_d = _converti_percorso(pos, percorsoCu)
        px_g, py_g = _converti_percorso(pos, percorsoGreedy)

        # Coordinate di partenza e destinazione
        fam_x, fam_y = converti_latlon_to_mercator(famiglia.lat, famiglia.lon)
        rif_x, rif_y = converti_latlon_to_mercator(rifugio.lat,  rifugio.lon)

        fig = plt.figure(figsize=(12, 11))
        # Creazione layout con due subplots: titolo in alto, mappa principale in basso
        gs  = gridspec.GridSpec(
            2, 1,
            figure=fig,
            height_ratios=[1, 11],
            hspace=0.04
        )
        ax_top = fig.add_subplot(gs[0])
        ax     = fig.add_subplot(gs[1])

        ax_top.set_axis_off()

        # Titolo della mappa
        ax_top.text(
            0.5, 1.15,
            f"PIANO DI FUGA PERSONALIZZATO\nNucleo: {famiglia.nome}",
            transform=ax_top.transAxes,
            ha='center', va='top',
            fontsize=14, fontweight='bold'
        )

        # Creazione legenda con i tre algoritmi e i marker di partenza/destinazione
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

        ax.plot(px_d, py_d, color='red',   linewidth=6, alpha=0.8, zorder=3)
        ax.plot(px_g, py_g, color='green', linewidth=4, alpha=0.8, zorder=4)
        # Traccio dei tre percorsi trovati dagli algoritmi
        ax.plot(px_a, py_a, color='blue',  linewidth=4, alpha=0.9, zorder=5)

        ax.scatter([fam_x], [fam_y], c='white', s=350, edgecolors='black',
                   linewidth=2, marker='o', zorder=7)
        # Marker della destinazione (rifugio)
        ax.scatter([rif_x], [rif_y], c='white', s=450, edgecolors='black',
                   linewidth=2, marker='P', zorder=7)

        all_x = px_a + px_d + px_g
        all_y = py_a + py_d + py_g
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)
        # Calcolo dei limiti della visualizzazione con padding per miglior visualizzazione
        pad_x = (max_x - min_x) * 0.15
        pad_y = (max_y - min_y) * 0.15
        ax.set_xlim(min_x - pad_x, max_x + pad_x)
        ax.set_ylim(min_y - pad_y, max_y + pad_y)
        ax.set_aspect('equal')

        try:
            # Aggiunta della base map (mappa di sfondo con OpenStreetMap)
            ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)
        except Exception as e:
            print(f"   Errore scaricamento sfondo: {e}")

        ax.set_axis_off()

        plt.savefig(
            f"mappa_{famiglia.nome.replace(' ', '_').replace('/', '-')}.png",
            dpi=150,
            bbox_inches='tight'
        )
        # Salvataggio e visualizzazione della mappa
        plt.show()
        plt.close(fig)

def visualizza_zona_rossa(cratere_lat=40.8224, cratere_lon=14.4289, raggio_km=4.5):
    # Visualizzazione della zona rossa (area di esclusione dal cratere del Vesuvio)
    fig, ax = plt.subplots(figsize=(10, 10))

    cx, cy = converti_latlon_to_mercator(cratere_lat, cratere_lon)
    # Creazione della zona rossa come cerchio di esclusione
    from matplotlib.patches import Circle
    cerchio = Circle((cx, cy), raggio_km*1000, color='red', alpha=0.3,
                     label=f'Zona Rossa {raggio_km}km')
    ax.add_patch(cerchio)
    ax.scatter([cx], [cy], c='darkred', s=200, marker='^',
               edgecolors='black', label='Cratere')

    margin = raggio_km * 1500
    ax.set_xlim(cx - raggio_km*1000 - margin, cx + raggio_km*1000 + margin)
    ax.set_ylim(cy - raggio_km*1000 - margin, cy + raggio_km*1000 + margin)

    # Aggiunta della base map
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, zoom=13)
    ax.set_axis_off()
    plt.title("Zona Rossa del Vesuvio", fontsize=14, fontweight='bold')
    plt.legend()
    plt.show()
