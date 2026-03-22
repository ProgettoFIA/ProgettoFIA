import os
import pickle
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from typing import List
from graph.graph_loader import scarica_grafo
from graph.graph_utils import get_nearest_node
from core.models import NucleoFamiliare, PuntoSicuro
from algorithms.selector import scegli_rifugio_migliore
from api.schemas import CalcoloRequest

grafo_globale = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global grafo_globale
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    file_mappa = os.path.join(project_root, "mappa_napoli.pkl")
    
    if os.path.exists(file_mappa):
        print(f"Caricamento del grafo dal file locale {file_mappa}...")
        with open(file_mappa, "rb") as f:
            grafo_globale = pickle.load(f)
        print("Mappa caricata istantaneamente!")
    else:
        print("ERRORE: mappa_napoli.pkl non trovato! Tentativo di download...")
        grafo_globale = scarica_grafo()
        
    yield
    print("Spegnimento del server FIA...")

app = FastAPI(title="Eruplan FIA Service", lifespan=lifespan)


@app.post("/calcola-percorso")
def calcola_percorso(req: CalcoloRequest):
    global grafo_globale
    if not grafo_globale:
        raise HTTPException(status_code=500, detail="Grafo non ancora inizializzato")
    fam = NucleoFamiliare(req.famiglia.nome, req.famiglia.lat, req.famiglia.lon, 
                          con_fragili=req.famiglia.con_fragili)
    
    rifugi_obj = []
    for r in req.rifugi:
        rif = PuntoSicuro(r.nome, r.lat, r.lon)
        rif.nodo_grafo = get_nearest_node(grafo_globale, rif.lat, rif.lon)
        rifugi_obj.append(rif)
        
    rif_migliore, percorso, tempo, exec_time, nodi_esplorati, tempo_miglior_rifugio = scegli_rifugio_migliore(
        grafo_globale, fam, rifugi_obj, algoritmo=req.algoritmo, tipo_euristica=req.euristica
    )
    
    if rif_migliore is None:
        return {"status": "error", "message": "Nessun percorso trovato per la famiglia."}
    
    coords_percorso = [{"lat": grafo_globale.nodes[n]['pos'][0], "lon": grafo_globale.nodes[n]['pos'][1]} for n in percorso]
      
    return {
        "status": "success",
        "rifugio_assegnato": rif_migliore.nome,
        "percorso_coordinate": coords_percorso,
        "tempo_stimato_minuti": int(tempo),
        "nodi_esplorati": nodi_esplorati,
        "tempo_esecuzione_ai_sec": tempo_miglior_rifugio
    }
