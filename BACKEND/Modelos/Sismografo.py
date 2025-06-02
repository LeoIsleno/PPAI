from .EstacionSismologica import EstacionSismologica
from .SerieTemporal import SerieTemporal
from .Estado import Estado
from .CambioEstado import CambioEstado

class Sismografo:
    def __init__(self, identificadorSismografo, nroSerie, fechaAdquisicion, estacionSismologica: EstacionSismologica, serieTemporal: SerieTemporal, estado: Estado = None, cambiosEstado=None):
        self.__identificadorSismografo = identificadorSismografo
        self.__nroSerie = nroSerie
        self.__fechaAdquisicion = fechaAdquisicion
        self.__estacionSismologica = estacionSismologica
        self.__serieTemporal = serieTemporal if serieTemporal is not None else []
        self.__estado = estado
        self.__cambiosEstado = cambiosEstado if cambiosEstado is not None else []

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
        if serieTemporal == self.__serieTemporal:
            return self.__estacionSismologica.getCodigoEstacion() #TODO: PUEDE QUE TAMBIEN SE TENGA QUE DEVOLVER DATOS DEL SISMOGRAFO
        return None

    def getEstado(self):
        return self.__estado

    def setEstado(self, estado):
        self.__estado = estado

    def getCambiosEstado(self):
        return self.__cambiosEstado

    def setCambiosEstado(self, cambios):
        self.__cambiosEstado = cambios

    def agregarCambioEstado(self, cambio: CambioEstado):
        self.__cambiosEstado.append(cambio)