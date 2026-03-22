from pydantic import BaseModel
from typing import List


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
    euristica: str = "euclidea"
