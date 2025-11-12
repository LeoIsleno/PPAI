from datetime import datetime
from Modelos.Estado import Estado
from Modelos.EventoSismico import EventoSismico
from Modelos.Sismografo import Sismografo
from Modelos.Sesion import Sesion
from Modelos.MagnitudRichter import MagnitudRichter
from BDD.database import SessionLocal
from BDD.repositories.evento_repository import EventoRepository

class GestorRevisionManual:
    def __init__(self):
        self.__eventosAutoDetectados = []
        self.__eventoSismicoSeleccionado = None
        self.__opcionMapaSeleccionada = None
        self.__opcionModificacionDatosSeleccionada = None
        self.__opcionEventoSeleccionada = None
        self._usuarioLogueado = None

    def opRegistrarResultadoRevisionManual(self, eventos):
        # Obtener los eventos de dominio que están en estado AutoDetectado,
        # ordenarlos por fecha de ocurrencia y devolver su representación
        # para la vista (mostrarDatosEventoSismico).
        eventos_auto = self.buscarEventosAutoDetectados(eventos)
        eventos_ordenados = self.ordenarESPorFechaOcurrencia(eventos_auto)
        return [e.mostrarDatosEventoSismico() for e in eventos_ordenados]

    def buscarEventosAutoDetectados(self, eventos):
        """
        Retorna la lista de objetos `EventoSismico` cuyo estado actual
        responde `esAutoDetectado()`.

        Usamos la delegación del patrón State: la consulta `estaAutoDetectado`
        del `EventoSismico` delega a `estadoActual.esAutoDetectado()`.
        """
        eventos_auto_detectado = []
        for evento in eventos:
            # Acceder explícitamente al estado actual y preguntar al estado
            # si es AutoDetectado. Evitamos usar el método de conveniencia
            # `evento.estaAutoDetectado()` para cumplir la petición.
            try:
                estado = None
                if hasattr(evento, 'getEstadoActual'):
                    estado = evento.getEstadoActual()
                if estado is not None and hasattr(estado, 'esAutoDetectado') and estado.esAutoDetectado():
                    eventos_auto_detectado.append(evento)
            except Exception:
                # Ignorar objetos mal formados en la colección
                continue
        return eventos_auto_detectado

    def ordenarESPorFechaOcurrencia(self, eventos: list[EventoSismico]):
        """
        Ordena una lista de `EventoSismico` por su fecha de ocurrencia
        (más recientes primero).
        """
        try:
            return sorted(eventos, key=lambda ev: ev.getFechaHoraOcurrencia() or datetime.min, reverse=True)
        except Exception:
            # En caso de que la lista no contenga EventoSismico u ocurra un
            # error al acceder a la fecha, devolver la lista tal cual.
            return eventos

    def buscarEstadoBloqueadoEnRevision(self, estados):
        for estado in estados:
            if estado.esAmbitoEventoSismico() and estado.esBloqueadoEnRevision():
                return estado
        return None

    def obtenerFechaHoraActual(self):
        return datetime.now()

    def bloquearEventoSismico(self, evento: EventoSismico, fecha_hora: datetime, usuario):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio.
        Este método recibe un `Usuario` y lo pasa a `EventoSismico.bloquear`, que se
        encargará de registrar el empleado asociado.
        """
        # La operación de bloqueo delega en el dominio; el dominio gestiona
        # el cambio de estado y el registro del responsable. Ya no se
        # devuelve ni se almacena un "último cambio" aquí.
        evento.bloquear(fecha_hora, usuario)

        # Usar context managers para que la sesión y la transacción se manejen
        # automáticamente (commit/rollback y close).
        with SessionLocal() as db:
            # `begin()` asegura commit automático o rollback en excepción
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return True
    

    def llamarCUGenerarSismograma(self, evento: EventoSismico):
        # Simulación de generación de sismograma
        # la implementación real no debe imprimir en consola
        return True


    def validarDatosMinimosRequeridos(self, evento):
        """
        Verifica que el evento tenga los datos mínimos requeridos.
        No captura excepciones generales aquí: si el dominio lanza una excepción
        debe propagarse; las únicas excepciones manejadas explícitamente en
        el gestor son las relativas a la persistencia (DB).

        Devuelve {'success': True} cuando está OK, o un dict de error cuando falta
        información requerida.
        """
        if evento is None:
            return {'success': False, 'error': 'Evento inválido', 'status_code': 400}

        magn = None
        magn_obj = evento.getMagnitud()
        if magn_obj is not None:
            # getNumero puede lanzar si el dominio está en un estado inconsistente;
            # dejamos que se propague en ese caso (no atrapamos aquí).
            magn = magn_obj.getNumero()

        if not (magn is not None and evento.getAlcanceSismo() and evento.getOrigenGeneracion()):
            return {'success': False, 'error': 'Faltan datos obligatorios del evento', 'status_code': 400}

        return {'success': True}
        
    def buscarASLogueado(self, sesion:Sesion):
        """
        Obtiene el usuario desde la sesión y verifica que el empleado asociado
        tenga rol de 'Administrador de Sismos'. Devuelve el objeto Usuario si
        está autorizado, o None si no lo está.
        """
        if sesion is None:
            return None

        usuario = sesion.obtenerUsuario()
        if usuario is None:
            return None

        # Delegar la comprobación de rol al propio Usuario (encapsula el acceso al Empleado)
        if usuario.esAdministradorSismos():
            return usuario

        return None
        

    def obtenerEstadoRechazado(self, estados):
        # Recorre todos los estados creados y verifica que sea de ámbito EventoSismico y que sea Rechazado
        for estado in estados:
            if estado.esAmbitoEventoSismico() and estado.esRechazado():
                return estado
        return None

    def obtenerEstadoConformado(self, estados):
        """Busca el estado ConfirmadoPorPersonal en la lista de estados"""
        for estado in estados:
            if estado.esAmbitoEventoSismico() and estado.esConfirmadoPorPersonal():
                return estado
        return None

    def obtenerEstadoDerivado(self, estados):
        """Busca el estado Derivado en la lista de estados"""
        for estado in estados:
            if estado.esAmbitoEventoSismico() and estado.esDerivado():
                return estado
        return None

    def rechazarEventoSismico(self, evento: EventoSismico, usuario, fecha_hora):
        evento.rechazar(fecha_hora, usuario)

        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return True
        
    def confirmarEventoSismico(self, evento: EventoSismico, usuario, fecha_hora):
        """
        Confirma un evento sísmico delegando en el dominio y persistiendo el cambio.
        Se mantiene la misma forma que `rechazarEventoSismico`: el método del gestor
        delega la lógica al dominio (`evento.confirmar`) y luego persiste usando
        `EventoRepository` dentro de una sesión.
        """
        # Delegar la confirmación al dominio. El dominio actualizará el
        # cambio/estado internamente; no guardamos un "último cambio" aquí.
        evento.confirmar(fecha_hora, usuario)

        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return True

    def derivarEventoSismico(self, evento: EventoSismico, usuario, fecha_hora):
        """
        Deriva un evento sísmico a experto delegando en el dominio y persistiendo el cambio.
        Similar a confirmarEventoSismico y rechazarEventoSismico, delega la lógica al
        dominio (`evento.derivar`) y luego persiste usando EventoRepository.
        """
        # Delegar la derivación al dominio.
        evento.derivar(fecha_hora, usuario)

        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return True
        

    def buscarDatosSismicos(self, evento: EventoSismico):
        datos_evento = evento.obtenerDatosSismicos()
        return datos_evento

    def buscarSeriesTemporales(self, evento: EventoSismico, sismografos: Sismografo):
        series_temporales = evento.obtenerSeriesTemporales(sismografos)
        return series_temporales

    def tomarSeleccionDeEventoSismico(self, eventos_persistentes, sismografos, data, usuario_logueado, estados):

        magnitud = data.get('magnitud')
        # The frontend may send a magnitud as a number or as an object like { numero: X, descripcion: Y }
        if isinstance(magnitud, dict):
            magnitud_val = magnitud.get('numero')
        else:
            magnitud_val = magnitud
        lat_epicentro = data.get('latEpicentro')
        long_epicentro = data.get('longEpicentro')
        lat_hipocentro = data.get('latHipocentro')
        long_hipocentro = data.get('longHipocentro')

        evento_seleccionado = next(
        (evento for evento in eventos_persistentes
         if (evento.getMagnitud() is not None and magnitud_val is not None and float(evento.getMagnitud().getNumero()) == float(magnitud_val))
         and float(evento.getLatitudEpicentro()) == float(lat_epicentro)
         and float(evento.getLongitudEpicentro()) == float(long_epicentro)
         and float(evento.getLatitudHipocentro()) == float(lat_hipocentro)
         and float(evento.getLongitudHipocentro()) == float(long_hipocentro)
        ),
        None
    )

        self.__eventoSismicoSeleccionado = evento_seleccionado

        if evento_seleccionado:
            # El estado no se busca, se crea en la transición
            usuario = self.buscarASLogueado(usuario_logueado)
            # Verificar que el usuario esté autorizado (empleado con rol administrador)
            if usuario is None:
                return {'success': False, 'error': 'Usuario no autorizado para bloquear eventos', 'status_code': 403}
            self._usuarioLogueado = usuario
            fec_hora = self.obtenerFechaHoraActual()

            # Intentar bloquear el evento (cambiar su estado)
            if self.bloquearEventoSismico(evento_seleccionado, fec_hora, usuario):
                evento_sismico = self.buscarDatosSismicos(evento_seleccionado)
                series_temportales = self.buscarSeriesTemporales(evento_seleccionado, sismografos)
                self.llamarCUGenerarSismograma(evento_seleccionado)
                return evento_sismico, series_temportales
            else:
                return {'success': False, 'error': 'Error al bloquear el evento', 'status_code': 500}
        else:
            return {'success': False, 'error': 'Evento no encontrado', 'status_code': 404}
            
    def tomarSeleccionOpcionEvento(self, data, estados):
        evento = self.__eventoSismicoSeleccionado
        if not evento:
            return {'success': False, 'error': 'No hay evento seleccionado', 'status_code': 404}

        accion = data.get('accion')

        if accion == 'rechazar':
            valid = self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)
            if not valid.get('success'):
                return valid

            fec_hora = self.obtenerFechaHoraActual()

            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            self.rechazarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, fec_hora)
            return {'success': True, 'mensaje': 'Evento rechazado correctamente'}
        
        elif accion == 'confirmar':
            valid = self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)
            if not valid.get('success'):
                return valid

            fec_hora = self.obtenerFechaHoraActual()

            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            self.confirmarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, fec_hora)
            return {'success': True, 'mensaje': 'Evento confirmado correctamente'}
        
        elif accion == 'experto':
            valid = self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)
            if not valid.get('success'):
                return valid

            fec_hora = self.obtenerFechaHoraActual()

            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            self.derivarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, fec_hora)
            return {'success': True, 'mensaje': 'Evento derivado a experto correctamente'}
        
        else:
            return {'success': False, 'error': 'Acción no válida', 'status_code': 400}

        
    def tomarSeleccionDeOpcionMapa(self):
        return '¹aqui mapa¹'
    
    def tomarOpcionModificacionDatos(self, request, lista_alcances, eventos_persistentes, lista_origenes):
        evento = self.__eventoSismicoSeleccionado
        if not evento:
            return {'success': False, 'error': 'No hay evento seleccionado', 'status_code': 404}
        data = request.json
        if 'magnitud' in data:
            # Accept either a numeric value or an object { numero: X, descripcion: Y }
            raw_magn = data['magnitud']
            if isinstance(raw_magn, dict):
                maybe_num = raw_magn.get('numero')
            else:
                maybe_num = raw_magn
            try:
                num = float(maybe_num) if maybe_num is not None else None
            except (ValueError, TypeError):
                num = None
            if num is not None:
                # crear o actualizar objeto MagnitudRichter
                if evento.getMagnitud() is None:
                    evento.setMagnitud(MagnitudRichter(None, num))
                else:
                    evento.getMagnitud().setNumero(num)
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
        
        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return {'success': True}
            





