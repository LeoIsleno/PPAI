from Modelos.estacion_sismologica import EstacionSismologica
from Modelos.serie_temporal import SerieTemporal

class Sismografo:
    def __init__(self, identificadorSismografo, nroSerie, fechaAdquisicion, estacionSismologica: EstacionSismologica, serieTemporal=None):
        self.__identificadorSismografo = identificadorSismografo
        self.__nroSerie = nroSerie
        self.__fechaAdquisicion = fechaAdquisicion
        self.__estacionSismologica = estacionSismologica
        self.__serieTemporal = serieTemporal if serieTemporal is not None else []

    # IdentificadorSismografo
    def getIdentificadorSismografo(self):
        return self.__identificadorSismografo

    def setIdentificadorSismografo(self, identificador):
        self.__identificadorSismografo = identificador

    # Getter y Setter para nroSerie
    def getNroSerie(self):
        return self.__nroSerie

    def setNroSerie(self, nroSerie):
        self.__nroSerie = nroSerie

    # Getter y Setter para fechaAdquisicion
    def getFechaAdquisicion(self):
        return self.__fechaAdquisicion

    def setFechaAdquisicion(self, fecha):
        self.__fechaAdquisicion = fecha

    # Getter y Setter para estacionSismologica
    def getEstacionSismologica(self):
        return self.__estacionSismologica

    def setEstacionSismologica(self, estacion):
        self.__estacionSismologica = estacion

    # Getter y Setter para serieTemporal
    def getSerieTemporal(self):
        return self.__serieTemporal

    def setSerieTemporal(self, serieTemporal):
        self.__serieTemporal = serieTemporal

    # Método para agregar una serie temporal
    def sosDeSerieTemporal(self, serieTemporal):
        self.__serieTemporal.append(serieTemporal)