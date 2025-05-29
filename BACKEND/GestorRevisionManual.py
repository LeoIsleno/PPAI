from datetime import datetime
from Modelos.Estado import Estado
from Modelos.EventoSismico import EventoSismico
from Modelos.CambioEstado import CambioEstado
from Modelos.AlcanceSismo import AlcanceSismo
from Modelos.ClasificacionSismo import ClasificacionSismo
from Modelos.OrigenDeGeneracion import OrigenDeGeneracion
from Modelos import DetalleMuestraSismica
from Modelos.MuestraSismica import MuestraSismica
from Modelos.SerieTemporal import SerieTemporal
from Modelos.TipoDeDato import TipoDeDato

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

    def buscarEventosAutoDetectados(self, eventos):
        eventosAutodetectados = []
        for evento in eventos:
            if evento.estaAutoDetectado():
                datosEvento = evento.mostrarDatosEventoSismico()
                eventosAutodetectados.append(datosEvento)
        return self.ordenarESPorFechaOcurrencia(eventosAutodetectados)

    def ordenarESPorFechaOcurrencia(self, eventos: list[EventoSismico]):
        return sorted(eventos, key=lambda x: x[0], reverse=True)

    def tomarSeleccionDeEvento(self, evento_id):
        # El evento ya viene seleccionado, solo guardarlo
        if evento_id:
            self.__eventoSismicoSeleccionado = evento_id
            return True
        return False

    def buscarEstadoBloqueadoEnRevision(self):
        # 1. Crear una nueva instancia del estado bloqueado
        estado = Estado("BloqueadoEnRevision")
        
        # 2. Validar que el estado sea del ámbito correcto y tenga el tipo correcto
        if estado.esBloqueadoEnRevision():
            return estado
        return None

    def obtenerFechaHoraActual(self):
        return self.__fechaHoraActual

    def bloquearEventoSismico(self, evento: EventoSismico, estadoBloqueado: Estado):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio
        """
        evento.bloquear(estadoBloqueado, self.__fechaHoraActual)  # Cambia el estado del evento a bloqueado con la fecha y hora actual
        

    def buscarDatosSismicos(self, evento):
        datos = evento.obtenerDatosSismicos(evento)  # Llama al método que obtiene los datos sísmicos del evento
       

    def buscarSeriesTemporales(self, evento: EventoSismico):
        datos_series = evento.obtenerSeriesTemporales(evento)  # Llama al método que obtiene las series temporales del evento
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
            # Validar datos mínimos
        if not (evento.getValorMagnitud() and evento.getAlcanceSismo() and evento.getOrigenGeneracion()):
            return jsonify({'success': False, 'error': 'Faltan datos obligatorios del evento'}), 400
        
    def buscarASLogueado(self, sesion):
        # Si sesion es un string (nombre de usuario), simplemente retorna ese string o crea un objeto Usuario si es necesario
        if isinstance(sesion, str):
            return sesion  # O puedes retornar Usuario(sesion, '', None) si necesitas el objeto
        # Si es un objeto de sesión, llama a obtenerUsuario()
        return sesion.obtenerUsuario()
        

    def obtenerEstadoRechazado(self):
        # 1. Crear una nueva instancia del estado rechazado
        estado = Estado("Rechazado")
        
        # 2. Validar solo que el estado sea rechazado
        if estado.esRechazado():
            return estado
        return None

    def buscarASLSismograma(self, evento: EventoSismico):
        print(f"Buscando ASL Sismograma para el evento ID {evento.id_evento}")
        return "Sismograma_Evento_" + str(evento.id_evento) # Simulación

    def rechazarEventoSismico(self, evento, usuario, estado_rechazado):
        evento.rechazar(estado_rechazado, self.__fechaHoraActual, usuario)  # Cambia el estado del evento a rechazado con la fecha y hora actual

    def opRegistrarResultadoRevisionManual(self, evento: EventoSismico):
        self.__pantallaRevision.opRegistrarResultadoRevisionManual(evento)

    def obtenerEventoSeleccionado(self):
        """Retorna el evento sísmico actualmente seleccionado"""
        return self.__eventoSismicoSeleccionado

    def tomarSeleccionEventoSismico(self,evento_seleccionado):
        if evento_seleccionado:
            # Buscar el estado 'BloqueadoEnRevision' para bloquear el evento
            estado_bloqueado = self.buscarEstadoBloqueadoEnRevision()
            
            if not estado_bloqueado:
                return jsonify({
                    'success': False,
                    'error': 'Error al crear el estado bloqueado'
                }, 500)

            # Intentar bloquear el evento (cambiar su estado)
            if self.bloquearEventoSismico(evento_seleccionado, estado_bloqueado):
                return jsonify({
                    'success': True,
                    'redirect': url_for('mostrar_datos_evento')
                })





