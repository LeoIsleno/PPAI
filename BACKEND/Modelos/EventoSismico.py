from datetime import datetime
from .SerieTemporal import SerieTemporal
from .Estado import Estado
from .ClasificacionSismo import ClasificacionSismo
from .OrigenDeGeneracion import OrigenDeGeneracion
from .AlcanceSismo import AlcanceSismo
from .CambioEstado import CambioEstado
from .Sismografo import Sismografo
from .MagnitudRichter import MagnitudRichter

class EventoSismico:
    def __init__(self, fechaHoraOcurrencia: datetime, latitudEpicentro, longitudEpicentro,
                  latitudHipocentro, longitudHipocentro, magnitud: MagnitudRichter, origenGeneracion: OrigenDeGeneracion, 
                  estadoActual: Estado, cambiosEstado: CambioEstado, clasificacion: ClasificacionSismo, 
                  alcanceSismo: AlcanceSismo, serieTemporal: SerieTemporal):
        
        self._fechaHoraOcurrencia = fechaHoraOcurrencia
        self._fechaHoraFin = None
        self._latitudEpicentro = latitudEpicentro
        self._longitudEpicentro = longitudEpicentro
        self._latitudHipocentro = latitudHipocentro
        self._longitudHipocentro = longitudHipocentro
        self._magnitud = magnitud
        self._origenGeneracion = origenGeneracion
        self._alcanceSismo = alcanceSismo
        self._clasificacion = clasificacion
        self._estadoActual = estadoActual
        self._cambiosEstado = cambiosEstado if isinstance(cambiosEstado, list) else [cambiosEstado]
        self._cambioEstadoActual = None
        
        for ce in self._cambiosEstado:
            if ce.getFechaHoraFin() is None:
                self._cambioEstadoActual = ce
                break
        self._serieTemporal = serieTemporal



    def getFechaHoraOcurrencia(self):
        return self._fechaHoraOcurrencia

    def setFechaHoraOcurrencia(self, value):
        self._fechaHoraOcurrencia = value

    def getFechaHoraFin(self):
        return self._fechaHoraFin

    def setFechaHoraFin(self, value):
        self._fechaHoraFin = value

    def getLatitudEpicentro(self):
        return self._latitudEpicentro

    def setLatitudEpicentro(self, value):
        self._latitudEpicentro = value

    def getLongitudEpicentro(self):
        return self._longitudEpicentro

    def setLongitudEpicentro(self, value):
        self._longitudEpicentro = value

    def getLatitudHipocentro(self):
        return self._latitudHipocentro

    def setLatitudHipocentro(self, value):
        self._latitudHipocentro = value

    def getLongitudHipocentro(self):
        return self._longitudHipocentro

    def setLongitudHipocentro(self, value):
        self._longitudHipocentro = value

    def getMagnitud(self):
        return self._magnitud

    def setMagnitud(self, magnitud: MagnitudRichter):
        self._magnitud = magnitud

    def getOrigenGeneracion(self):
        return self._origenGeneracion

    def setOrigenGeneracion(self, value):
        self._origenGeneracion = value

    def getClasificacion(self):
        return self._clasificacion

    def setClasificacion(self, value):
        self._clasificacion = value

    def getEstadoActual(self):
        return self._estadoActual

    def setEstado(self, value):
        self._estadoActual = value

    def setEstadoActual(self, estado: Estado):
        """Alias a setEstado para compatibilidad."""
        self.setEstado(estado)

    def setCambioEstadoActual(self, cambio: CambioEstado):
        """Establece cuál es el cambio de estado actual del evento (no persiste)."""
        self._cambioEstadoActual = cambio

    def getCambiosEstado(self):
        return self._cambiosEstado

    def setCambiosEstado(self, value):
        self._cambiosEstado = value

    def getAlcanceSismo(self):
        return self._alcanceSismo

    def setAlcanceSismo(self, value):
        self._alcanceSismo = value

    def getSerieTemporal(self):
        return self._serieTemporal

    def setSerieTemporal(self, value):
        self._serieTemporal = value

    def estaAutoDetectado(self):
        return self._estadoActual.esAutoDetectado()

    def mostrarDatosEventoSismico(self):
        # Devuelve una representación compacta para listados: fecha, lat_epic, lon_epic, lat_hipo, lon_hipo, magnitud_obj
        magn = None
        if isinstance(self._magnitud, MagnitudRichter):
            magn = { 'numero': self._magnitud.getNumero(), 'descripcion': self._magnitud.getDescripcionMagnitud() }
        return [self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S'),
                self.getLatitudEpicentro(),
                self.getLongitudEpicentro(),
                self.getLatitudHipocentro(),
                self.getLongitudHipocentro(),
                magn]

    def obtenerDatosSismicos(self):
        """Obtiene los datos sísmicos completos del evento seleccionado recorriendo explícitamente las relaciones"""
        
        nombre_alcance = self._alcanceSismo.getNombre() if self._alcanceSismo else 'No disponible'
        descripcion_alcance = self._alcanceSismo.getDescripcion() if self._alcanceSismo else 'No disponible'
        nombre_clasificacion = self._clasificacion.getNombre() if self._clasificacion else 'No disponible'
        nombre_origen = self._origenGeneracion.getNombre() if self._origenGeneracion else 'No disponible'
    
        magnitud_info = None
        if isinstance(self._magnitud, MagnitudRichter):
            magnitud_info = {
                'numero': self._magnitud.getNumero(),
                'descripcion': self._magnitud.getDescripcionMagnitud()
            }
        fecha_hora = self._fechaHoraOcurrencia
        lat_epicentro = self._latitudEpicentro
        long_epicentro = self._longitudEpicentro
        lat_hipocentro = self._latitudHipocentro
        long_hipocentro = self._longitudHipocentro
        
        datos = {
            'alcanceSismo': nombre_alcance,
            'clasificacion': nombre_clasificacion,
            'origenGeneracion': nombre_origen,
            'descripcionAlcance': descripcion_alcance,
            'magnitud': magnitud_info,
            'fechaHoraOcurrencia': fecha_hora.strftime('%Y-%m-%d %H:%M:%S') if fecha_hora else 'No disponible',
            'latitudEpicentro': str(lat_epicentro) if lat_epicentro is not None else 'No disponible',
            'longitudEpicentro': str(long_epicentro) if long_epicentro is not None else 'No disponible',
            'latitudHipocentro': str(lat_hipocentro) if lat_hipocentro is not None else 'No disponible',
            'longitudHipocentro': str(long_hipocentro) if long_hipocentro is not None else 'No disponible'
        }
        return datos

    def obtenerSeriesTemporales(self, sismografos: Sismografo):
        """
        Devuelve una lista con los datos de todas las series temporales asociadas al evento,
        usando el método getDatos() de cada serie temporal.
        """
        series = self._serieTemporal
        datos_series = []
        for serie in series:
            datos = serie.getDatos(sismografos) 
            datos_series.append(datos)
        return datos_series
    
    def obtenerCambioEstadoActual(self):
        """
        Obtiene el cambio de estado que se considera actual (sin fecha de fin).
        """
        return self._cambioEstadoActual

    def crearCambioEstado(self, estado: Estado, fechaHoraActual: datetime, usuario):
        """
        Crea un CambioEstado registrando el `Usuario` que efectuó el cambio.
        """
        nuevo_cambio = CambioEstado(fechaHoraActual, estado, usuario)
        self._cambiosEstado.append(nuevo_cambio)
        return nuevo_cambio
    
    def bloquear (self, fechaHoraActual: datetime, usuario):
        """Realiza el bloqueo del evento.

        Delegamos la lógica de transición al objeto `Estado` recibido.
        Esto respeta la estructura UML: la decisión/efecto de la transición
        queda encapsulada en la jerarquía de estados.
        """
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede bloquear")
        return self._estadoActual.bloquear(self, fechaHoraActual, usuario)
    
    def rechazar(self, fechaHoraActual: datetime, usuario):
        """
        Cambia el estado del evento a 'Rechazado', cierra el estado actual y registra el cambio.
        """
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede rechazar")
        return self._estadoActual.rechazar(self, fechaHoraActual, usuario)

    def confirmar(self, fechaHoraActual: datetime, usuario):
        """Confirmar el evento: delega al objeto Estado si implementa la operación."""
        # Delegar al estado actual del evento para procesar la confirmación.
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede confirmar")
        return self._estadoActual.confirmar(self, fechaHoraActual, usuario)

    def derivar(self, fechaHoraActual: datetime, usuario):
        """Derivar el evento a experto: delega al objeto Estado si implementa la operación."""
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede derivar")
        return self._estadoActual.derivar(self, fechaHoraActual, usuario)


        


