from config import VELOCITA_AUTO, VELOCITA_PIEDI, VELOCITA_FRAGILI


class NucleoFamiliare:
    def __init__(self, nome, lat, lon, in_auto=False, con_fragili=False):
        self.nome = nome
        self.lat = lat
        self.lon = lon
        self.in_auto = in_auto
        self.con_fragili = con_fragili

        if self.in_auto:
            self.speed_ms = VELOCITA_AUTO / 3.6
            self.descrizione = "[AUTO] Veicolo"
        elif self.con_fragili:
            self.speed_ms = VELOCITA_FRAGILI / 3.6
            self.descrizione = "[LENTO] A Piedi (Anziani)"
        else:
            self.speed_ms = VELOCITA_PIEDI / 3.6
            self.descrizione = "[VELOCE] A Piedi"


class PuntoSicuro:
    def __init__(self, nome, lat, lon):
        self.nome = nome
        self.lat = lat
        self.lon = lon
        self.nodo_grafo = None
