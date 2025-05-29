from datetime import datetime
from .SerieTemporal import SerieTemporal
from .Estado import Estado
from .ClasificacionSismo import ClasificacionSismo
from .OrigenDeGeneracion import OrigenDeGeneracion
from .AlcanceSismo import AlcanceSismo
from .CambioEstado import CambioEstado

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
        return self._estadoActual.esAutoDetectado()

    def mostrarDatosEventoSismico(self):
        return [self.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S'),
                self.getLatitudEpicentro(),
                self.getLongitudEpicentro(),
                self.getLatitudHipocentro(),
                self.getLongitudHipocentro(),
                self.getValorMagnitud()]

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
        """Obtiene los datos sísmicos completos del evento seleccionado recorriendo explícitamente las relaciones"""
        # Acceso explícito a cada relación
        alcance = self.getAlcanceSismo()
        clasificacion = self.getClasificacion()
        origen = self.getOrigenGeneracion()
        descripcion_alcance = alcance.getDescripcion() if alcance else 'No disponible'
        nombre_alcance = alcance.getNombre() if alcance else 'No disponible'
        nombre_clasificacion = clasificacion.getNombre() if clasificacion else 'No disponible'
        nombre_origen = origen.getNombre() if origen else 'No disponible'
        valor_magnitud = self.getValorMagnitud()
        fecha_hora = self.getFechaHoraOcurrencia()
        lat_epicentro = self.getLatitudEpicentro()
        long_epicentro = self.getLongitudEpicentro()
        lat_hipocentro = self.getLatitudHipocentro()
        long_hipocentro = self.getLongitudHipocentro()
        
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
        print("Datos obtenidos:", datos)
        return datos

    def obtenerSeriesTemporales(self):
        """
        Devuelve una lista con los datos de todas las series temporales asociadas al evento,
        usando el método getDatos() de cada serie temporal.
        """
        series = self.getSerieTemporal()
        datos_series = []
        for serie in series:
            datos = serie.getDatos()  # Suponiendo que getDatos() retorna un dict o similar
            datos_series.append(datos)
        return datos_series
            
    
        

    def rechazar(self, estadoRechazado: Estado, fechaHoraActual: datetime, usuario):
        """
        Cambia el estado del evento a 'Rechazado', cierra el estado actual y registra el cambio.
        """
        # 1. Buscar el cambio de estado actual (el que está activo)
        cambio_actual = None
        for cambio in self.getCambiosEstado():
            if cambio is not None and cambio.esEstadoActual():
                cambio_actual = cambio
                break

        # 2. Cerrar el cambio de estado actual (ponerle fecha de fin)
        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        # 3. Crear y agregar el nuevo cambio de estado (rechazado)
        nuevo_cambio = CambioEstado(fechaHoraActual, estadoRechazado, usuario)
        self.getCambiosEstado().append(nuevo_cambio)

        # 4. Actualizar el estado actual del evento
        self.setEstadoActual(estadoRechazado)

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
    
    def bloquear (estadoBloqueado: Estado, fechaHoraActual: datetime):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio
        """

        self.setEstadoActual(estadoBloqueado)
        
        cambio_actual = None
        for cambio in self.getCambiosEstado():
            if cambio is not None and cambio.esEstadoActual():
                cambio_actual = cambio
                break
            
        CambioEstado.setFechaHoraFin(cambio_actual, fechaHoraActual) 
        # Asegurarse de que el cambio actual no tenga fecha de fin
        
        nuevo_cambio = CambioEstado(fechaHoraActual, estadoBloqueado)
        self.getCambiosEstado().append(nuevo_cambio)



