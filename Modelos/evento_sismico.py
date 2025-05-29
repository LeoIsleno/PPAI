from datetime import datetime
from .serie_temporal import SerieTemporal
from .estado import Estado
from .clasificacion_sismo import ClasificacionSismo
from .origen_de_generacion import OrigenDeGeneracion
from .alcance_sismo import AlcanceSismo
from .cambio_estado import CambioEstado

class EventoSismico:
    def __init__(self, fechaHoraOcurrencia: datetime, latitudEpicentro, longitudEpicentro,
                  latitudHipocentro, longitudHipocentro, valorMagnitud, origenGeneracion: OrigenDeGeneracion, 
                  estadoActual: Estado, cambiosEstado: CambioEstado, clasificacion: ClasificacionSismo, 
                  alcanceSismo: AlcanceSismo, serieTemporal: SerieTemporal):
        
        self._fechaHoraOcurrencia = fechaHoraOcurrencia
        self._fechaHoraFin = None
        self._latitudEpicentro = latitudEpicentro
        self._longitudEpicentro = longitudEpicentro
        self._latitudHipocentro = latitudHipocentro
        self._longitudHipocentro = longitudHipocentro
        self._valorMagnitud = valorMagnitud
        self._origenGeneracion = origenGeneracion
        self._alcanceSismo = alcanceSismo
        self._clasificacion = clasificacion
        self._estadoActual = estadoActual
        self._cambiosEstado = cambiosEstado if isinstance(cambiosEstado, list) else [cambiosEstado]
        self._serieTemporal = serieTemporal

    # Fecha Ocurrencia
    def getFechaHoraOcurrencia(self):
        return self._fechaHoraOcurrencia

    def setFechaHoraOcurrencia(self, value):
        self._fechaHoraOcurrencia = value

    # Fecha Fin
    def getFechaHoraFin(self):
        return self._fechaHoraFin

    def setFechaHoraFin(self, value):
        self._fechaHoraFin = value

    # Latitud Epicentro
    def getLatitudEpicentro(self):
        return self._latitudEpicentro

    def setLatitudEpicentro(self, value):
        self._latitudEpicentro = value

    # Longitud Epicentro
    def getLongitudEpicentro(self):
        return self._longitudEpicentro

    def setLongitudEpicentro(self, value):
        self._longitudEpicentro = value

    # Latitud Hipocentro
    def getLatitudHipocentro(self):
        return self._latitudHipocentro

    def setLatitudHipocentro(self, value):
        self._latitudHipocentro = value

    # Longitud Hipocentro
    def getLongitudHipocentro(self):
        return self._longitudHipocentro

    def setLongitudHipocentro(self, value):
        self._longitudHipocentro = value

    # Valor Magnitud
    def getValorMagnitud(self):
        return self._valorMagnitud

    def setValorMagnitud(self, value):
        self._valorMagnitud = value

    # Origen Generacion
    def getOrigenGeneracion(self):
        return self._origenGeneracion

    def setOrigenGeneracion(self, value):
        self._origenGeneracion = value

    # Clasificacion
    def getClasificacion(self):
        return self._clasificacion

    def setClasificacion(self, value):
        self._clasificacion = value

    # Estado Actual
    def getEstadoActual(self):
        return self._estadoActual

    def setEstadoActual(self, value):
        self._estadoActual = value

    # Cambios Estado
    def getCambiosEstado(self):
        """Retorna la lista de cambios de estado"""
        return self._cambiosEstado

    def setCambiosEstado(self, value):
            self._cambiosEstado = value

     # Alcance Sismo
    def getAlcanceSismo(self):
        return self._alcanceSismo

    def setAlcanceSismo(self, value):
        self._alcanceSismo = value

    # Serie Temporal
    def getSerieTemporal(self):
        return self._serieTemporal

    def setSerieTemporal(self, value):
        self._serieTemporal = value




    def estaAutoDetectado(self):
        return self._estadoActual.esAutoDetectado("EventoSismico")

    def mostrarDatosEventoSismico(self):
        return (
            f"--- Evento Sísmico ---\n"
            f"Fecha y Hora: {self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Latitud Epicentro: {self.getLatitudEpicentro()}\n"
            f"Longitud Epicentro: {self.getLongitudEpicentro()}\n"
            f"Latitud Hipocentro: {self.getLatitudHipocentro()}\n"
            f"Longitud Hipocentro: {self.getLongitudHipocentro()}\n"
            f"Magnitud: {self.getValorMagnitud()}\n"
            f"----------------------"
        )

    def bloquear(self):
        estado_bloqueado = Estado("BloqueadoEnRevision", "EventoSismico")
        self.crearCambioEstado(estado_bloqueado)

    def obtenerEstadoActual(self):
        return self.estadoActual

    def crearCambioEstado(self, nuevoEstado: Estado):
        # Crear nuevo cambio de estado
        cambio = CambioEstado(datetime.now(), nuevoEstado, self)
        # Agregar a la lista de cambios
        self._cambiosEstado.append(cambio)
        # Actualizar el estado actual
        self._estadoActual = nuevoEstado

    def obtenerDatosSismicos(self):
        pass

    def obtenerSeriesTemporales(self):
        pass

    def rechazar(self):
        estado_rechazado = Estado("Rechazado", "EventoSismico")
        self.crearCambioEstado(estado_rechazado)

    def bloquearEvento(self, estadoBloqueado: Estado):
        # Validar que el estado sea el correcto
        if estadoBloqueado.esBloqueadoEnRevision() and estadoBloqueado.esAmbitoEventoSismico():
            # Crear el cambio de estado
            self.crearCambioEstado(estadoBloqueado)
            return True
        return False

    def getDatos(self):
        alcance = self.getAlcanceSismo()
        clasificacion = self.getClasificacion()
        origen = self.getOrigenGeneracion()
        return {
            'alcanceSismo': alcance.getNombre() if alcance else 'No disponible',
            'clasificacion': clasificacion.getNombre() if clasificacion else 'No disponible',
            'origenGeneracion': origen.getNombre() if origen else 'No disponible',
            'descripcionAlcance': alcance.getDescripcion() if alcance else 'No disponible',
            'valorMagnitud': str(self.getValorMagnitud()),
            'fechaHoraOcurrencia': self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S') if self.getFechaHoraOcurrencia() else 'No disponible',
            'latitudEpicentro': str(self.getLatitudEpicentro()) if self.getLatitudEpicentro() is not None else 'No disponible',
            'longitudEpicentro': str(self.getLongitudEpicentro()) if self.getLongitudEpicentro() is not None else 'No disponible',
            'latitudHipocentro': str(self.getLatitudHipocentro()) if self.getLatitudHipocentro() is not None else 'No disponible',
            'longitudHipocentro': str(self.getLongitudHipocentro()) if self.getLongitudHipocentro() is not None else 'No disponible',
            'series_temporales': [serie.getDatos() for serie in self.getSerieTemporal()] if isinstance(self.getSerieTemporal(), list) else [self.getSerieTemporal().getDatos()]
        }
