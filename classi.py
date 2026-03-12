from config import VELOCITA_AUTO


class NucleoFamiliare:
    def __init__(self, nome, lat, lon, con_fragili=False):
        self.nome = nome
        self.lat = lat
        self.lon = lon
        self.con_fragili = con_fragili

        #convertire velocità da km/h a m/s
        self.speed_ms = VELOCITA_AUTO / 3.6




class PuntoSicuro:
    def __init__(self, nome, lat, lon, capacita_max=10):
        self.nome = nome
        self.lat = lat
        self.lon = lon
        self.nodo_grafo = None


        self.capacita_max = capacita_max
        self.famiglie_assegnate = 0

    def isPieno(self):
        return self.famiglie_assegnate >= self.capacita_max

    def aggiungiFamiglia(self):
        if not self.isPieno():
            self.famiglie_assegnate += 1
            if self.isPieno():
                print("ATTENZIONE: Il Punto Sicuro '{self.nome}' si è totalmente riempito!")
                return True
            return False
