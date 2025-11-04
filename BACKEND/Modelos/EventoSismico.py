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
        # Referencia explícita al cambio de estado actual (el que tenga fechaHoraFin == None)
        self._cambioEstadoActual = None
        # si en la lista de cambios hay uno abierto (fechaHoraFin es None), usarlo
        try:
            for ce in self._cambiosEstado:
                if hasattr(ce, 'getFechaHoraFin'):
                    if ce.getFechaHoraFin() is None:
                        self._cambioEstadoActual = ce
                        break
        except Exception:
            # En casos donde los objetos no tienen la API esperada, dejamos None
            self._cambioEstadoActual = None
        self._serieTemporal = serieTemporal

    def __str__(self):
        mag = None
        if isinstance(self._magnitud, MagnitudRichter):
            mag = self._magnitud.getNumero()
        return f"Evento Sismico: {self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S')} - Magnitud: {mag}"

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
    # Acceso al objeto MagnitudRichter
    def getMagnitud(self):
        return self._magnitud

    def setMagnitud(self, magnitud: MagnitudRichter):
        self._magnitud = magnitud

    # NOTE: legacy numeric access removed. Use getMagnitud()/setMagnitud() to work with MagnitudRichter objects.

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

    def setEstadoActual(self, estado: Estado):
        """Método requerido por la dinámica: ajusta el estado actual del evento."""
        # Mantener alias hacia setEstado para compatibilidad
        self.setEstado(estado)

    def setCambioEstadoActual(self, cambio: CambioEstado):
        """Establece cuál es el cambio de estado actual del evento.

        No realiza persistencia, solo actualiza la referencia en memoria.
        """
        self._cambioEstadoActual = cambio

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

        # borre lo del cambio de estado de aca

    def obtenerDatosSismicos(self): #TODO: ESTE MEDTODO ESTA RETORNANDO COSAS DE MAS, O LE BORRAMOS COSAS O LO CAMBIAMOS EN EL DIAG DE SECUENCIA
        """Obtiene los datos sísmicos completos del evento seleccionado recorriendo explícitamente las relaciones"""
        # Acceso explícito a cada relación
        nombre_alcance = self._alcanceSismo.getNombre() if self._alcanceSismo else 'No disponible'
        descripcion_alcance = self._alcanceSismo.getDescripcion() if self._alcanceSismo else 'No disponible'
        nombre_clasificacion = self._clasificacion.getNombre() if self._clasificacion else 'No disponible'
        nombre_origen = self._origenGeneracion.getNombre() if self._origenGeneracion else 'No disponible'
    # info completa de magnitud para el frontend (compatibilidad)
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
        """Realiza el bloqueo del evento.

        Delegamos la lógica de transición al objeto `Estado` recibido.
        Esto respeta la estructura UML: la decisión/efecto de la transición
        queda encapsulada en la jerarquía de estados.
        """
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede bloquear")
        return self._estadoActual.bloquear(self, fechaHoraActual, usuario)
    
    def rechazar(self, estadoRechazado: Estado, fechaHoraActual: datetime, usuario, ult_cambio: CambioEstado):
        """
        Cambia el estado del evento a 'Rechazado', cierra el estado actual y registra el cambio.
        """
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede rechazar")
        return self._estadoActual.rechazar(self, fechaHoraActual, usuario, ult_cambio)

    def confirmar(self, estadoConfirmado: Estado, fechaHoraActual: datetime, usuario, ult_cambio: CambioEstado = None):
        """Confirmar el evento: delega al objeto Estado si implementa la operación."""
        # Delegar al estado actual del evento para procesar la confirmación.
        if self._estadoActual is None:
            raise RuntimeError("Evento sin estado actual: no se puede confirmar")
        return self._estadoActual.confirmar(self, fechaHoraActual, usuario, ult_cambio)


        


