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
        self.__seriesTemporales = serieTemporal
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
        return self.__seriesTemporales

    def setSerieTemporal(self, serieTemporal):
        self.__seriesTemporales = serieTemporal

    # Método para agregar una serie temporal
    def sosDeSerieTemporal(self, serieTemporal):
        # Intent: no confiar en identidad de objetos (se crean instancias distintas
        # al mapear desde ORM). Comparar por atributos que identifican la serie.
        for serie in self.__seriesTemporales:
            try:
                # Comparar por fecha de registro cuando esté disponible
                if hasattr(serie, 'getFechaHoraRegistro') and hasattr(serieTemporal, 'getFechaHoraRegistro'):
                    if serie.getFechaHoraRegistro() == serieTemporal.getFechaHoraRegistro():
                        return {
                            'codigoEstacion': self.__estacionSismologica.getCodigoEstacion(),
                            'nombreEstacion': self.__estacionSismologica.getNombre()
                        }

                # Fallback: comparar por frecuencia de muestreo
                if hasattr(serie, 'getFrecuenciaMuestreo') and hasattr(serieTemporal, 'getFrecuenciaMuestreo'):
                    if serie.getFrecuenciaMuestreo() == serieTemporal.getFrecuenciaMuestreo():
                        return {
                            'codigoEstacion': self.__estacionSismologica.getCodigoEstacion(),
                            'nombreEstacion': self.__estacionSismologica.getNombre()
                        }
            except Exception:
                # Si alguna comparación falla, continuar con la siguiente serie
                continue
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