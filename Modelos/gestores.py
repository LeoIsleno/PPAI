from datetime import datetime
from .estado import Estado
from .evento_sismico import EventoSismico
from .cambio_estado import CambioEstado
from .alcance_sismo import AlcanceSismo
from .clasificacion_sismo import ClasificacionSismo
from .origen_de_generacion import OrigenDeGeneracion
from .detalle_muestra_sismica import DetalleMuestraSismica
from .muestra_sismica import MuestraSismica
from .serie_temporal import SerieTemporal
from .tipo_de_dato import TipoDeDato

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
        # 1. Crear una nueva instancia del estado bloqueado
        estado = Estado("BloqueadoEnRevision", "EventoSismico")
        
        # 2. Validar que el estado sea del ámbito correcto y tenga el tipo correcto
        if estado.esAmbitoEventoSismico() and estado.esBloqueadoEnRevision():
            return estado
        return None

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
        """Obtiene los datos sísmicos completos del evento seleccionado recorriendo explícitamente las relaciones"""
        try:
            print("Buscando datos sísmicos para evento:", id(evento))
            # Acceso explícito a cada relación
            alcance = evento.getAlcanceSismo()
            clasificacion = evento.getClasificacion()
            origen = evento.getOrigenGeneracion()
            descripcion_alcance = alcance.getDescripcion() if alcance else 'No disponible'
            nombre_alcance = alcance.getNombre() if alcance else 'No disponible'
            nombre_clasificacion = clasificacion.getNombre() if clasificacion else 'No disponible'
            nombre_origen = origen.getNombre() if origen else 'No disponible'
            valor_magnitud = evento.getValorMagnitud()
            fecha_hora = evento.getFechaHoraOcurrencia()
            lat_epicentro = evento.getLatitudEpicentro()
            long_epicentro = evento.getLongitudEpicentro()
            lat_hipocentro = evento.getLatitudHipocentro()
            long_hipocentro = evento.getLongitudHipocentro()
            
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
        except Exception as e:
            print(f"Error obteniendo datos sísmicos: {str(e)}")
            return {}

    def obtenerSeriesTemporales(self, evento: EventoSismico):
        """
        Devuelve la lista de series temporales del evento, usando el método getDatos() recursivo de cada serie temporal.
        """
        series = evento.getSerieTemporal()
        if not isinstance(series, list):
            series = [series]
        datos_series = []
        for serie in series:
            # Formatear fechas solo hasta los segundos
            fecha_inicio = serie.getFechaHoraInicioRegistroMuestras()
            fecha_registro = serie.getFechaHoraRegistro()
            serie_dict = serie.getDatos()
            if fecha_inicio:
                serie_dict['fechaHoraInicioRegistroMuestras'] = fecha_inicio.strftime('%Y-%m-%d %H:%M:%S')
            if fecha_registro:
                serie_dict['fechaHoraRegistro'] = fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
            # Formatear fechas de muestras
            for muestra in serie_dict['muestras']:
                try:
                    dt = muestra['fechaHoraMuestra']
                    if isinstance(dt, str) and ' ' in dt:
                        # Ya es string
                        muestra['fechaHoraMuestra'] = dt[:19]
                except Exception:
                    pass
            datos_series.append(serie_dict)
        return datos_series

    def llamarCUGenerarSismograma(self, evento: EventoSismico):
        # Simulación de generación de sismograma
        print(f"Generando sismograma para el evento ID {getattr(evento, 'id_evento', '?')}")
        return True

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
        # 1. Crear una nueva instancia del estado rechazado
        estado = Estado("Rechazado", "EventoSismico")
        
        # 2. Validar que el estado sea del ámbito correcto y tenga el tipo correcto
        if estado.esAmbitoEventoSismico() and estado.esRechazado():
            return estado
        return None

    def buscarASLSismograma(self, evento: EventoSismico):
        print(f"Buscando ASL Sismograma para el evento ID {evento.id_evento}")
        return "Sismograma_Evento_" + str(evento.id_evento) # Simulación

    def rechazarEventoSismico(self, evento, usuario):
        estado_rechazado = Estado("Rechazado", "EventoSismico")
        evento.crearCambioEstado(estado_rechazado)
        evento.setFechaHoraFin(datetime.now())
        print(f"El evento ID {getattr(evento, 'id_evento', '?')} ha sido rechazado por {usuario} a las {datetime.now()}")

    def opRegistrarResultadoRevisionManual(self, evento: EventoSismico):
        self.__pantallaRevision.opRegistrarResultadoRevisionManual(evento)

    def obtenerEventoSeleccionado(self):
        """Retorna el evento sísmico actualmente seleccionado"""
        return self.__eventoSismicoSeleccionado


