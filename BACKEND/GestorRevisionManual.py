from datetime import datetime
from Modelos.Estado import Estado
from Modelos.EventoSismico import EventoSismico
from Modelos.Sismografo import Sismografo
from Modelos.Sesion import Sesion
from flask import jsonify

class GestorRevisionManual:
    def __init__(self):
        self.__eventosAutoDetectados = []
        self.__eventoSismicoSeleccionado = None
        self.__opcionMapaSeleccionada = None
        self.__opcionModificacionDatosSeleccionada = None
        self.__opcionEventoSeleccionada = None
        self._usuarioLogueado = None


    def opRegistrarResultadoRevisionManual(self, eventos):
        eventos_auto_det = self.buscarEventosAutoDetectados(eventos)
        return self.ordenarESPorFechaOcurrencia(eventos_auto_det)

    def buscarEventosAutoDetectados(self, eventos):
        eventos_auto_detectado = []
        for evento in eventos:
            if evento.estaAutoDetectado():
                datos_evento = evento.mostrarDatosEventoSismico()
                eventos_auto_detectado.append(datos_evento)
        return eventos_auto_detectado

    def ordenarESPorFechaOcurrencia(self, eventos: list[EventoSismico]):
        return sorted(eventos, key=lambda x: x[0], reverse=True)

    def buscarEstadoBloqueadoEnRevision(self, estados):
        for estado in estados:
            if estado.esAmbitoEventoSismico() and estado.esBloqueadoEnRevision():
                return estado
        return None

    def obtenerFechaHoraActual(self):
        return datetime.now()

    def bloquearEventoSismico(self, evento: EventoSismico, estado_bloqueado: Estado, fecha_hora: datetime, usuario):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio
        """
        self.__ultimo_cambio = evento.bloquear(estado_bloqueado, fecha_hora, usuario)  # Cambia el estado del evento a bloqueado con la fecha y hora actual
        return True 
    

    def llamarCUGenerarSismograma(self, evento: EventoSismico):
        # Simulación de generación de sismograma
        print(f"Generando sismograma para el evento ID {getattr(evento, 'id_evento', '?')}")
        return True


    def validarDatosMinimosRequeridos(self, evento):
            # Validar datos mínimos
        if not (evento.getValorMagnitud() and evento.getAlcanceSismo() and evento.getOrigenGeneracion()):
            return jsonify({'success': False, 'error': 'Faltan datos obligatorios del evento'}), 400
        
    def buscarASLogueado(self, sesion:Sesion):
        
        return sesion.obtenerUsuario()
        

    def obtenerEstadoRechazado(self, estados):
        # Recorre todos los estados creados y verifica que sea de ámbito EventoSismico y que sea Rechazado
        for estado in estados:
            if estado.esAmbitoEventoSismico() and estado.esRechazado():
                return estado
        return None

    def rechazarEventoSismico(self, evento: EventoSismico, usuario, estado_rechazado, fecha_hora, ult_cambio):
        evento.rechazar(estado_rechazado, fecha_hora, usuario, ult_cambio)  # Cambia el estado del evento a rechazado con la fecha y hora actual

    def buscarDatosSismicos(self, evento: EventoSismico):
        datos_evento = evento.obtenerDatosSismicos()
        return datos_evento

    def buscarSeriesTemporales(self, evento: EventoSismico, sismografos: Sismografo):
        series_temporales = evento.obtenerSeriesTemporales(sismografos)
        return series_temporales

    def tomarSeleccionDeEventoSismico(self, eventos_persistentes, sismografos, data, usuario_logueado, estados):

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
            estado_bloqueado = self.buscarEstadoBloqueadoEnRevision(estados)
            usuario = self.buscarASLogueado(usuario_logueado)
            self._usuarioLogueado = usuario
            fec_hora = self.obtenerFechaHoraActual()
            if not estado_bloqueado:
                return jsonify({
                    'success': False,
                    'error': 'Error al crear el estado bloqueado'
                }, 500)

            # Intentar bloquear el evento (cambiar su estado)
            if self.bloquearEventoSismico(evento_seleccionado, estado_bloqueado, fec_hora, usuario):
                evento_sismico = self.buscarDatosSismicos(evento_seleccionado)
                series_temportales = self.buscarSeriesTemporales(evento_seleccionado, sismografos)
                self.llamarCUGenerarSismograma(evento_seleccionado)
                return evento_sismico, series_temportales
            
    def tomarSeleccionOpcionEvento(self, data, estados):
        evento = self.__eventoSismicoSeleccionado
        if not evento:
            return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404

        accion = data.get('accion')

        if accion == 'rechazar':
            self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)

            estado_rechazado = self.obtenerEstadoRechazado(estados)

            fec_hora = self.obtenerFechaHoraActual()
            
            self.rechazarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, estado_rechazado, fec_hora, self.__ultimo_cambio)
            return jsonify({'success': True, 'mensaje': 'Evento rechazado correctamente'})
        elif accion == 'confirmar':
            return jsonify({'success': True, 'mensaje': 'Evento confirmado correctamente'})
        elif accion == 'experto':
            return jsonify({'success': True, 'mensaje': 'Revisión a experto solicitada'})
        else:
            return jsonify({'success': False, 'error': 'Acción no válida'}), 400
        
    def tomarSeleccionDeOpcionMapa(self):
        return '¹aqui mapa¹'
    
    def tomarOpcionModificacionDatos(self, request, lista_alcances, eventos_persistentes, lista_origenes):
        evento = self.__eventoSismicoSeleccionado
        if not evento:
            return jsonify({'success': False, 'error': 'No hay evento seleccionado'}), 404
        data = request.json
        if 'valorMagnitud' in data:
            evento.setValorMagnitud(data['valorMagnitud'])
        if 'alcanceSismo' in data:
            alcances = lista_alcances
            alcance = next((a for a in alcances if a.getNombre() == data['alcanceSismo']), None)
            if alcance:
                evento.setAlcanceSismo(alcance)
        if 'origenGeneracion' in data:
            origenes = lista_origenes
            origen = next((o for o in origenes if o.getNombre() == data['origenGeneracion']), None)
            if origen:
                evento.setOrigenGeneracion(origen)
        # --- Actualiza el evento en la lista persistente si es necesario ---
        for idx, ev in enumerate(eventos_persistentes):
            if ev is evento:
                eventos_persistentes[idx] = evento
                break
        return jsonify({'success': True})
            





