from datetime import datetime
from BACKEND.Modelos.Estado import Estado
from BACKEND.Modelos.EventoSismico import EventoSismico
from BACKEND.Modelos.Sismografo import Sismografo
from BACKEND.Modelos.Sesion import Sesion
from BACKEND.Modelos.MagnitudRichter import MagnitudRichter
from BDD.database import SessionLocal
from BDD.repositories.evento_repository import EventoRepository
from BACKEND.Modelos.Usuario import Usuario

class GestorRevisionManual:
    def __init__(self):
        self.__eventosAutoDetectados = []
        self.__eventoSismicoSeleccionado = None
        self.__opcionMapaSeleccionada = None
        self.__opcionModificacionDatosSeleccionada = None
        self.__opcionEventoSeleccionada = None
        self._usuarioLogueado = None
        self._fechaHoraActual = None

    def opRegistrarResultadoRevisionManual(self, eventos):
        # Obtener los eventos de dominio que están en estado AutoDetectado,
        # ordenarlos por fecha de ocurrencia y devolver su representación
        # para la vista (mostrarDatosEventoSismico).
        self.__eventosAutoDetectados = self.buscarEventosAutoDetectados(eventos)
        eventos_ordenados = self.ordenarESPorFechaOcurrencia(self.__eventosAutoDetectados)
        return [e.mostrarDatosEventoSismico() for e in eventos_ordenados]

    def buscarEventosAutoDetectados(self, eventos):
        eventos_auto_detectado = []
        for evento in eventos:
            try:
                # Cambio: comprobar tipo y llamar directamente al método
                if evento.estaAutoDetectado():
                    eventos_auto_detectado.append(evento)
            except Exception:
                # Ignorar objetos mal formados en la colección
                continue
        return eventos_auto_detectado

    def ordenarESPorFechaOcurrencia(self, eventos: list[EventoSismico]):
        return sorted(eventos, key=lambda ev: ev.getFechaHoraOcurrencia() or datetime.min, reverse=True)

    def obtenerFechaHoraActual(self):
        return datetime.now()

    def bloquearEventoSismico(self):
        """
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio.
        Este método recibe un `Usuario` y lo pasa a `EventoSismico.bloquear`, que se
        encargará de registrar el empleado asociado.
        """
        evento:EventoSismico = self.__eventoSismicoSeleccionado
        evento.bloquear(self._fechaHoraActual, self._usuarioLogueado)

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
        
    def buscarASLogueado(self):
        """
        Obtiene el usuario desde la sesión y verifica que el empleado asociado
        tenga rol de 'Administrador de Sismos'. Devuelve el objeto Usuario si
        está autorizado, o None si no lo está.
        """

        usuario = self._usuarioLogueado
        if usuario is None:
            return None

        # Delegar la comprobación de rol al propio Usuario (encapsula el acceso al Empleado)
        if usuario.esAnalistaSismos():
            return usuario

        return None
        



    def rechazarEventoSismico(self):
        evento:EventoSismico = self.__eventoSismicoSeleccionado
        evento.rechazar(self._fechaHoraActual, self._usuarioLogueado)

        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return True

    def confirmarEventoSismico(self):
        """
        Confirma un evento sísmico delegando en el dominio y persistiendo el cambio.
        Se mantiene la misma forma que `rechazarEventoSismico`: el método del gestor
        delega la lógica al dominio (`evento.confirmar`) y luego persiste usando
        `EventoRepository` dentro de una sesión.
        """
        # Delegar la confirmación al dominio. El dominio actualizará el
        # cambio/estado internamente; no guardamos un "último cambio" aquí.
        evento:EventoSismico = self.__eventoSismicoSeleccionado
        evento.confirmar(self._fechaHoraActual, self._usuarioLogueado)

        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return True

    def derivarEventoSismico(self):
        """
        Deriva un evento sísmico a experto delegando en el dominio y persistiendo el cambio.
        Similar a confirmarEventoSismico y rechazarEventoSismico, delega la lógica al
        dominio (`evento.derivar`) y luego persiste usando EventoRepository.
        """
        # Delegar la derivación al dominio.
        evento:EventoSismico = self.__eventoSismicoSeleccionado
        evento.derivar(self._fechaHoraActual, self._usuarioLogueado)

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

    def tomarSeleccionDeEventoSismico(self, sismografos, data, usuario_logueado, estados):

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

        print(  f"Buscando evento con magnitud={magnitud_val}, "
                f"lat_epicentro={lat_epicentro}, long_epicentro={long_epicentro}, "
                f"lat_hipocentro={lat_hipocentro}, long_hipocentro={long_hipocentro}")
        
        for e in self.__eventosAutoDetectados:
            print(f" - Evento ID={e.getId()}, Magnitud={e.getMagnitud().getNumero() if e.getMagnitud() else 'N/A'}, "
                  f"LatEpicentro={e.getLatitudEpicentro()}, LongEpicentro={e.getLongitudEpicentro()}, "
                  f"LatHipocentro={e.getLatitudHipocentro()}, LongHipocentro={e.getLongitudHipocentro()}")

        evento_seleccionado = next(
            (evento for evento in self.__eventosAutoDetectados
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
            usuario = self.buscarASLogueado()
            # Verificar que el usuario esté autorizado (empleado con rol administrador)
            if usuario is None:
                return {'success': False, 'error': 'Usuario no autorizado para bloquear eventos', 'status_code': 403}
            self._usuarioLogueado = usuario
            self._fechaHoraActual = self.obtenerFechaHoraActual()

            # Intentar bloquear el evento (cambiar su estado)
            if self.bloquearEventoSismico():
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

        self.__opcionEventoSeleccionada = data.get('accion')

        if self.__opcionEventoSeleccionada == 'rechazar':
            valid = self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)
            if not valid.get('success'):
                return valid

            self._fechaHoraActual = self.obtenerFechaHoraActual()

            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            if self.rechazarEventoSismico():
                return {'success': True, 'mensaje': 'Evento rechazado correctamente'}
            return {'success': False, 'error': 'Error al rechazar el evento', 'status_code': 500}
        
        elif self.__opcionEventoSeleccionada == 'confirmar':
            valid = self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)
            if not valid.get('success'):
                return valid

            self._fechaHoraActual = self.obtenerFechaHoraActual()

            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            if self.confirmarEventoSismico():
                return {'success': True, 'mensaje': 'Evento confirmado correctamente'}
            return {'success': False, 'error': 'Error al confirmar el evento', 'status_code': 500}  
        
        elif self.__opcionEventoSeleccionada == 'experto':
            valid = self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)
            if not valid.get('success'):
                return valid

            self._fechaHoraActual = self.obtenerFechaHoraActual()

            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            if self.derivarEventoSismico():
                return {'success': True, 'mensaje': 'Evento derivado a experto correctamente'}
            return {'success': False, 'error': 'Error al derivar el evento', 'status_code': 500}
        
        else:
            return {'success': False, 'error': 'Acción no válida', 'status_code': 400}

        
    def tomarSeleccionDeOpcionMapa(self):
        return '¹aqui mapa¹'
    
    def tomarOpcionModificacionDatos(self, request, lista_alcances, lista_origenes):
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
            num = float(maybe_num) if maybe_num is not None else None
            if num is not None:
                # crear o actualizar objeto MagnitudRichter
                if evento.getMagnitud() is None:
                    evento.setMagnitud(MagnitudRichter(None, num))
                else:
                    evento.getMagnitud().setNumero(num)
        if 'alcanceSismo' in data:
            alcances = lista_alcances
            alcance = next((a for a in alcances if a.getNombre() == data['alcanceSismo']), None)
            # Si no existe un objeto de dominio correspondiente en la lista
            # (por ejemplo cuando el frontend envía strings simples), crear
            # un objeto `AlcanceSismo` ligero para asignarlo al evento.
            if alcance:
                evento.setAlcanceSismo(alcance)
            else:
                from Modelos.AlcanceSismo import AlcanceSismo
                # data['alcanceSismo'] puede ser None o string; solo crear si existe
                if data['alcanceSismo']:
                    evento.setAlcanceSismo(AlcanceSismo(None, data['alcanceSismo']))
        if 'origenGeneracion' in data:
            origenes = lista_origenes
            origen = next((o for o in origenes if o.getNombre() == data['origenGeneracion']), None)
            if origen:
                evento.setOrigenGeneracion(origen)
            else:
                from Modelos.OrigenDeGeneracion import OrigenDeGeneracion
                if data['origenGeneracion']:
                    evento.setOrigenGeneracion(OrigenDeGeneracion(data['origenGeneracion'], None))
        # --- Actualiza el evento en la lista persistente si es necesario ---
        for idx, ev in enumerate(self.__eventosAutoDetectados):
            if ev is evento:
                self.__eventosAutoDetectados[idx] = evento
                break
        
        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)

        return {'success': True}
    
    def setSesionUsuarioLogueado(self, sesion: Sesion):
        self._usuarioLogueado = sesion.obtenerUsuario()

    def cancelarRevisionEventoSismico(self):
        """
        Coordina la cancelación de la revisión, revirtiendo el evento 
        al estado AutoDetectado y persistiendo el cambio.
        """
        evento:EventoSismico = self.__eventoSismicoSeleccionado
        if not evento:
            return False

        # 1. Actualizar fecha y usuario
        self._fechaHoraActual = self.obtenerFechaHoraActual()
        usuario = self._usuarioLogueado
        
        # 2. Delegar la lógica de transición al dominio
        try:
            evento.volver(self._fechaHoraActual, usuario)
        except NotImplementedError:
            # Si el estado actual (ej: Rechazado) no permite cancelar
            return False 
        
        # 3. Persistir cambios (siempre dentro de la sesión/transacción)
        with SessionLocal() as db:
            with db.begin():
                EventoRepository.from_domain(db, evento)
        
        # 4. Limpiar selección interna para el próximo uso
        self.__eventoSismicoSeleccionado = None 
        return True 






