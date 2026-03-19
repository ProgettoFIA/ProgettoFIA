import requests
import networkx as nx
from config import BBOX_NAPOLI
from utils import dist_metri


def scarica_grafo():
    print("Download mappa ...")
    url = "https://lz4.overpass-api.de/api/interpreter"
    query = f'[out:json][timeout:500];(way["highway"]({BBOX_NAPOLI});node(w););out body;'

    try:
        resp = requests.post(url, data={"data": query}, timeout=500)
        resp.raise_for_status()
        dati = resp.json()
    except Exception as e:
        print(f"Errore API: {e}")
        return None

    print(f"Costruzione Grafo NetworkX...")
    G = nx.Graph()
    nodes_temp = {}

    for el in dati.get('elements', []):
        if el['type'] == 'node':
            G.add_node(str(el['id']), pos=(el['lat'], el['lon']))
            nodes_temp[str(el['id'])] = (el['lat'], el['lon'])

    for el in dati.get('elements', []):
        if el['type'] == 'way' and 'nodes' in el:
            wn = el['nodes']
            for i in range(len(wn) - 1):
                u, v = str(wn[i]), str(wn[i + 1])
                if u in nodes_temp and v in nodes_temp:
                    dist = dist_metri(nodes_temp[u][0], nodes_temp[u][1],
                                      nodes_temp[v][0], nodes_temp[v][1])
                    G.add_edge(u, v, weight=dist)

    print(f"Grafo pronto! {G.number_of_nodes()} nodi.")
    return G

def zoneRosse(G,crater_lat=40.8224, crater_lon=14.4289, raggio_km=4.5):
    """Identifica i nodi del grafo che si trovano all'interno del raggio del Vesuvio e li esclude."""
    print(f"\n🌋 ATTIVAZIONE ZONA ROSSA: Chiusura strade entro {raggio_km}km dal cratere...")
    nodi_zone_rosse = []
    for n, data in G.nodes(data=True):
        lat, lon = data['pos']
        distanza_km = dist_metri(lat, lon, crater_lat, crater_lon) / 1000
        if distanza_km <= raggio_km:
            nodi_zone_rosse.append(n)
    G.remove_nodes_from(nodi_zone_rosse)
    print(f"🛑 Rimosse {len(nodi_zone_rosse)} intersezioni pericolose dal grafo!")

    return G


def get_nearest_node(G, lat, lon):
    """Trova il nodo del grafo più vicino a una coordinata GPS."""
    return min(G.nodes(data=True),
               key=lambda n: (n[1]['pos'][0] - lat) ** 2 + (n[1]['pos'][1] - lon) ** 2)[0]
