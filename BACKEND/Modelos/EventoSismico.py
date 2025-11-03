from datetime import datetime
from .SerieTemporal import SerieTemporal
from .Estado import Estado
from .ClasificacionSismo import ClasificacionSismo
from .OrigenDeGeneracion import OrigenDeGeneracion
from .AlcanceSismo import AlcanceSismo
from .CambioEstado import CambioEstado
from .Sismografo import Sismografo

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

    def __str__(self):
        return f"Evento Sismico: {self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S')} - Magnitud: {self.getValorMagnitud()}"

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

    def setEstado(self, value):
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
        return self._estadoActual.esAutoDetectado()

    def mostrarDatosEventoSismico(self):
        return [self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S'),
                self.getLatitudEpicentro(),
                self.getLongitudEpicentro(),
                self.getLatitudHipocentro(),
                self.getLongitudHipocentro(),
                self.getValorMagnitud()]

        # borre lo del cambio de estado de aca

    def obtenerDatosSismicos(self): #TODO: ESTE MEDTODO ESTA RETORNANDO COSAS DE MAS, O LE BORRAMOS COSAS O LO CAMBIAMOS EN EL DIAG DE SECUENCIA
        """Obtiene los datos sísmicos completos del evento seleccionado recorriendo explícitamente las relaciones"""
        # Acceso explícito a cada relación
        nombre_alcance = self._alcanceSismo.getNombre() if self._alcanceSismo else 'No disponible'
        descripcion_alcance = self._alcanceSismo.getDescripcion() if self._alcanceSismo else 'No disponible'
        nombre_clasificacion = self._clasificacion.getNombre() if self._clasificacion else 'No disponible'
        nombre_origen = self._origenGeneracion.getNombre() if self._clasificacion else 'No disponible'
        valor_magnitud = self._valorMagnitud
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
            'valorMagnitud': str(valor_magnitud),
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
    
    def obtnerEstadoActual(self):
        for cambio in self._cambiosEstado:
            if cambio.esEstadoActual():
                return cambio
                
    def crearCambioEstado(self, estado: Estado, fechaHoraActual: datetime, usuario):
        """
        Crea un CambioEstado registrando el `Usuario` que efectuó el cambio.
        """
        nuevo_cambio = CambioEstado(fechaHoraActual, estado, usuario)
        self._cambiosEstado.append(nuevo_cambio)
        return nuevo_cambio
    
    def bloquear (self, estadoBloqueado: Estado, fechaHoraActual: datetime, usuario):

        self.setEstado(estadoBloqueado)

        cambio_actual = self.obtnerEstadoActual()

        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        return self.crearCambioEstado(estadoBloqueado, fechaHoraActual, usuario)
    
    def rechazar(self, estadoRechazado: Estado, fechaHoraActual: datetime, usuario, ult_cambio: CambioEstado):
        """
        Cambia el estado del evento a 'Rechazado', cierra el estado actual y registra el cambio.
        """

        self.setEstado(estadoRechazado)

        if ult_cambio:
            ult_cambio.setFechaHoraFin(fechaHoraActual)

        return self.crearCambioEstado(estadoRechazado, fechaHoraActual, usuario)

        


