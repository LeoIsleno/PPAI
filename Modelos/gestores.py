from datetime import datetime
from .estado import Estado
from .evento_sismico import EventoSismico
from .cambio_estado import CambioEstado

class GestorRevisionManual:
    def __init__(self):
        self.__eventosAutoDetectados = []
        self.__eventoSismicoSeleccionado = None
        self.__estadoBloqueadoEnRevision = None
        self.__fechaHoraActual = datetime.now()
        self.__datosSismicos = None
        self.__seriesTemporales = []
        self.__opcionMapaSeleccionada = None
        self.__opcionModificacionDatosSeleccionada = None
        self.__opcionEventoSeleccionada = None
        self.__estadoRechazado = None
        self.__analistaEnSismosLogueado = None


    def agregarEventoAutoDetectado(self, evento: EventoSismico):
        self.__eventosAutoDetectados.append(evento)

    def buscarEventosAutoDetectados(self):
        return [e for e in self.__eventosAutoDetectados if e.estaAutoDetectado()]

    def ordenarESPorFechaOcurrencia(self, eventos: list[EventoSismico]):
        return sorted(eventos, key=lambda x: x.getFechaHoraOcurrencia())

    def tomarSeleccionDeEvento(self, evento_id):
        # El evento ya viene seleccionado, solo guardarlo
        if evento_id:
            self.__eventoSismicoSeleccionado = evento_id
            return True
        return False

    def buscarEstadoBloqueadoEnRevision(self):
        # Crear una nueva instancia del estado bloqueado
        return Estado("BloqueadoEnRevision", "EventoSismico")

    def obtenerFechaHoraActual(self):
        return self.__fechaHoraActual

    def bloquearEventoSismico(self, evento: EventoSismico, estadoBloqueado: Estado):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio
        """
        try:
            if evento and estadoBloqueado:
                # 1. Guardar el evento seleccionado en el gestor
                self.__eventoSismicoSeleccionado = evento
                
                # 2. Obtener los cambios de estado del evento
                cambios_estado = evento.getCambiosEstado()
                
                # 3. Buscar el cambio de estado actual (sin fecha fin)
                cambio_actual = next(
                    (cambio for cambio in cambios_estado if cambio.getFechaHoraHasta() is None),
                    None
                )
                
                if cambio_actual:
                    # 4. Establecer la fecha fin del estado actual
                    fecha_hora_actual = datetime.now()
                    cambio_actual.setFechaHoraHasta(fecha_hora_actual)
                    
                    # 5. Crear nuevo cambio de estado con estado bloqueado
                    nuevo_cambio = CambioEstado(
                        fechaHoraDesde=fecha_hora_actual,
                        estado=estadoBloqueado
                    )
                    
                    # 6. Agregar el nuevo cambio al evento y actualizar estado actual
                    evento.getCambiosEstado().append(nuevo_cambio)
                    evento.setEstadoActual(estadoBloqueado)
                    
                    return True
                    
            return False
        except Exception as e:
            print(f"Error bloqueando evento: {str(e)}")
            return False

    def buscarDatosSismicos(self, evento):
        """Obtiene los datos sísmicos completos del evento seleccionado"""
        try:
            # Imprimir para debug
            print("Buscando datos sísmicos para evento:", id(evento))
            
            datos = {
                'alcanceSismo': evento.getAlcanceSismo().getNombre() if evento.getAlcanceSismo() else 'No disponible',
                'clasificacion': evento.getClasificacion().getNombre() if evento.getClasificacion() else 'No disponible',
                'origenGeneracion': evento.getOrigenGeneracion().getNombre() if evento.getOrigenGeneracion() else 'No disponible',
                'descripcionAlcance': evento.getAlcanceSismo().getDescripcion() if evento.getAlcanceSismo() else 'No disponible',
                'valorMagnitud': str(evento.getValorMagnitud()),
                'fechaHoraOcurrencia': evento.getFechaHoraOcurrencia().strftime('%Y-%m-%d %H:%M:%S'),
                'latitudEpicentro': str(evento.getLatitudEpicentro()),
                'longitudEpicentro': str(evento.getLongitudEpicentro()),
                'latitudHipocentro': str(evento.getLatitudHipocentro()),
                'longitudHipocentro': str(evento.getLongitudHipocentro())
            }
            
            # Imprimir para debug
            print("Datos obtenidos:", datos)
            return datos
            
        except Exception as e:
            print(f"Error obteniendo datos sísmicos: {str(e)}")
            return {}

    def buscarSeriesTemporales(self, evento: EventoSismico):
        series = evento.getSerieTemporal()
        return self.procesarSeriesTemporales(series)

    def procesarSeriesTemporales(self, series):
        datos_series = []
        for serie in series:
            datos_series.append({
                'fecha': serie.getFechaHoraRegistro(),
                'muestras': self.procesarMuestras(serie.getMuestraSismica())
            })
        return datos_series

    def llamarCUGenerarSismograma(self, evento: EventoSismico):
        print(f"Llamando al caso de uso para generar sismograma del evento ID {evento.id_evento}")
        # Lógica para generar el sismograma

    def tomarSeleccionDeOpcionMapa(self):
        self.__opcionMapaSeleccionada = self.__pantallaRevision.mostrarOpcionMapa()
        return self.__opcionMapaSeleccionada

    def tomarSeleccionDeOpcionModificacionDatos(self):
        self.__opcionModificacionDatosSeleccionada = self.__pantallaRevision.mostrarOpcionModificacionDatos()
        return self.__opcionModificacionDatosSeleccionada

    def tomarSeleccionDeOpcionEvento(self):
        self.__opcionEventoSeleccionada = self.__pantallaRevision.pedirOpcionEvento()
        return self.__opcionEventoSeleccionada

    def validarDatosMinimosRequeridos(self, evento):
        return (evento.getValorMagnitud() and 
                evento.getAlcanceSismo() and 
                evento.getOrigenGeneracion())

    def obtenerEstadoRechazado(self):
        return Estado(ambito="evento", nombre="rechazado", es_auto_detectado=False,
                      es_bloqueado_revision=False, es_ambito_revision=False, es_rechazado=True, es_finalizado=True)

    def buscarASLSismograma(self, evento: EventoSismico):
        print(f"Buscando ASL Sismograma para el evento ID {evento.id_evento}")
        return "Sismograma_Evento_" + str(evento.id_evento) # Simulación

    def rechazarEventoSismico(self, evento):
        estado_rechazado = Estado("Rechazado", "EventoSismico")
        evento.crearCambioEstado(estado_rechazado)
        evento.setFechaHoraFin(datetime.now())
        print(f"El evento ID {evento.id_evento} ha sido rechazado.")

    def opRegistrarResultadoRevisionManual(self, evento: EventoSismico):
        self.__pantallaRevision.opRegistrarResultadoRevisionManual(evento)

    def obtenerEventoSeleccionado(self):
        """Retorna el evento sísmico actualmente seleccionado"""
        return self.__eventoSismicoSeleccionado


