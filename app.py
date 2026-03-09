from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from network import scarica_grafo, get_nearest_node
from classi import NucleoFamiliare, PuntoSicuro
from AI import scegli_rifugio_migliore
import pickle
import os

app = FastAPI(title="Eruplan FIA Service")

grafo_globale = None

import os
import pickle
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from network import scarica_grafo, get_nearest_node
from classi import NucleoFamiliare, PuntoSicuro
from AI import scegli_rifugio_migliore

grafo_globale = None

# NUOVO METODO LIFESPAN
@asynccontextmanager
async def lifespan(app: FastAPI):
    global grafo_globale
    file_mappa = "mappa_napoli.pkl"
    
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
class FamigliaData(BaseModel):
    nome: str
    lat: float
    lon: float
    in_auto: bool = False
    con_fragili: bool = False

class RifugioData(BaseModel):
    nome: str
    lat: float
    lon: float

class CalcoloRequest(BaseModel):
    famiglia: FamigliaData
    rifugi: List[RifugioData]
    algoritmo: str = "A*"

# Endpoint principale esposto all'Adapter del modulo GPE
@app.post("/calcola-percorso")
def calcola_percorso(req: CalcoloRequest):
    global grafo_globale
    if not grafo_globale:
        raise HTTPException(status_code=500, detail="Grafo non ancora inizializzato")
    fam = NucleoFamiliare(req.famiglia.nome, req.famiglia.lat, req.famiglia.lon, 
                          req.famiglia.in_auto, req.famiglia.con_fragili)
    rifugi_obj = []
    for r in req.rifugi:
        rif = PuntoSicuro(r.nome, r.lat, r.lon)
        rif.nodo_grafo = get_nearest_node(grafo_globale, rif.lat, rif.lon)
        rifugi_obj.append(rif)
    rif_migliore, percorso, tempo, exec_time = scegli_rifugio_migliore(
        grafo_globale, fam, rifugi_obj, algoritmo=req.algoritmo
    )
    if rif_migliore is None:
        return {"status": "error", "message": "Nessun percorso trovato per la famiglia."}
    return {
        "status": "success",
        "famiglia": fam.nome,
        "rifugio_assegnato": rif_migliore.nome,
        "tempo_stimato_minuti": round(tempo, 2),
        "tempo_esecuzione_ai_sec": round(exec_time, 4),
        "percorso_nodi": percorso
    }