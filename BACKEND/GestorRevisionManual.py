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
from Modelos.Sismografo import Sismografo
from flask import jsonify, url_for

class GestorRevisionManual:
    def __init__(self):
        self.__eventosAutoDetectados = []
        self.__eventoSismicoSeleccionado = None
        self.__estadoBloqueadoEnRevision = None
        self.__datosSismicos = None
        self.__seriesTemporales = []
        self.__opcionMapaSeleccionada = None
        self.__opcionModificacionDatosSeleccionada = None
        self.__opcionEventoSeleccionada = None
        self.__estadoRechazado = None
        self.__analistaEnSismosLogueado = None
        self.__ultimo_cambio = None


    def opRegistrarResultadoRevisionManual(self, eventos):
        eventosAutoDet = self.buscarEventosAutoDetectados(eventos)
        return self.ordenarESPorFechaOcurrencia(eventosAutoDet)

    def agregarEventoAutoDetectado(self, evento: EventoSismico):
        self.__eventosAutoDetectados.append(evento)

    def buscarEventosAutoDetectados(self, eventos):
        eventosAutodetectados = []
        for evento in eventos:
            if evento.estaAutoDetectado():
                datosEvento = evento.mostrarDatosEventoSismico()
                eventosAutodetectados.append(datosEvento)
        return eventosAutodetectados

    def ordenarESPorFechaOcurrencia(self, eventos: list[EventoSismico]):
        return sorted(eventos, key=lambda x: x[0], reverse=True)

    def buscarEstadoBloqueadoEnRevision(self):
        for estado in Estado.estados_creados:
            if estado.esAmbitoEventoSismico() and estado.esBloqueadoEnRevision():
                return estado
        return None

    def obtenerFechaHoraActual(self):
        return datetime.now()

    def bloquearEventoSismico(self, evento: EventoSismico, estado_bloqueado: Estado, facha_hora: datetime, usuario):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio
        """
        self.__ultimo_cambio = evento.bloquear(estado_bloqueado, facha_hora, usuario)  # Cambia el estado del evento a bloqueado con la fecha y hora actual
        return True 
    
       

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
        # Recorre todos los estados creados y verifica que sea de ámbito EventoSismico y que sea Rechazado
        for estado in Estado.estados_creados:
            if estado.esAmbitoEventoSismico() and estado.esRechazado():
                return estado
        return None

    def buscarASLSismograma(self, evento: EventoSismico):
        print(f"Buscando ASL Sismograma para el evento ID {evento.id_evento}")
        return "Sismograma_Evento_" + str(evento.id_evento) # Simulación

    def rechazarEventoSismico(self, evento, usuario, estado_rechazado, fecha_hora, ult_cambio):
        evento.rechazar(estado_rechazado, fecha_hora, usuario, ult_cambio)  # Cambia el estado del evento a rechazado con la fecha y hora actual

    # def opRegistrarResultadoRevisionManual(self, evento: EventoSismico):
    #     self.__pantallaRevision.opRegistrarResultadoRevisionManual(evento)

    def obtenerEventoSeleccionado(self):
        """Retorna el evento sísmico actualmente seleccionado"""
        return self.__eventoSismicoSeleccionado

    def buscarDatosSismicos(self, evento: EventoSismico):
        datos_evento = evento.obtenerDatosSismicos()
        return datos_evento

    def buscarSeriesTemporales(self, evento: EventoSismico, sismografos: Sismografo):
        series_temporales = evento.obtenerSeriesTemporales(sismografos)
        return series_temporales

    def tomarSeleccionDeEventoSismico(self, eventos_persistentes, sismografos, data, usuario):

        magnitud = data.get('magnitud')
        lat_epicentro = data.get('latEpicentro')
        long_epicentro = data.get('longEpicentro')
        lat_hipocentro = data.get('latHipocentro')
        long_hipocentro = data.get('longHipocentro')

        evento_seleccionado = next(
        (evento for evento in eventos_persistentes
         if float(evento.getValorMagnitud()) == float(magnitud)
         and float(evento.getLatitudEpicentro()) == float(lat_epicentro)
         and float(evento.getLongitudEpicentro()) == float(long_epicentro)
         and float(evento.getLatitudHipocentro()) == float(lat_hipocentro)
         and float(evento.getLongitudHipocentro()) == float(long_hipocentro)
        ),
        None
    )

        self.__eventoSismicoSeleccionado = evento_seleccionado

        if evento_seleccionado:
            # Buscar el estado 'BloqueadoEnRevision' para bloquear el evento
            estado_bloqueado = self.buscarEstadoBloqueadoEnRevision()
            fec_hora = self.obtenerFechaHoraActual()
            if not estado_bloqueado:
                return jsonify({
                    'success': False,
                    'error': 'Error al crear el estado bloqueado'
                }, 500)

            # Intentar bloquear el evento (cambiar su estado)
            if self.bloquearEventoSismico(evento_seleccionado, estado_bloqueado, fec_hora, usuario):
                evento_sismico, series_temportales = self.buscarDatosSismicos(evento_seleccionado), self.buscarSeriesTemporales(evento_seleccionado, sismografos)
                self.llamarCUGenerarSismograma(evento_seleccionado)
                return evento_sismico, series_temportales
            
    def tomarSeleccionOpcionEvento(self, data, usuario):
        accion = data.get('accion')

        if accion == 'rechazar':
            self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)

            estado_rechazado = self.obtenerEstadoRechazado()

            usuario_obj = self.buscarASLogueado(usuario)

            fec_hora = self.obtenerFechaHoraActual()
            
            self.rechazarEventoSismico(self.__eventoSismicoSeleccionado, usuario_obj, estado_rechazado, fec_hora, self.__ultimo_cambio)
            return jsonify({'success': True, 'mensaje': 'Evento rechazado correctamente'})
        elif accion == 'confirmar':
            return jsonify({'success': True, 'mensaje': 'Evento confirmado correctamente'})
        elif accion == 'experto':
            return jsonify({'success': True, 'mensaje': 'Revisión a experto solicitada'})
        else:
            return jsonify({'success': False, 'error': 'Acción no válida'}), 400
            





