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
        Bloquea un evento sísmico cambiando su estado actual y registrando el cambio.
        Este método recibe un `Usuario` y lo pasa a `EventoSismico.bloquear`, que se
        encargará de registrar el empleado asociado.
        """
        self.__ultimo_cambio = evento.bloquear(estado_bloqueado, fecha_hora, usuario)

        db = SessionLocal()
        try:
            EventoRepository.from_domain(db, evento)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

        return True
    

    def llamarCUGenerarSismograma(self, evento: EventoSismico):
        # Simulación de generación de sismograma
        print(f"Generando sismograma para el evento ID {getattr(evento, 'id_evento', '?')}")
        return True


    def validarDatosMinimosRequeridos(self, evento):
        magn = None
        try:
            magn_obj = evento.getMagnitud()
            magn = magn_obj.getNumero() if magn_obj else None
        except Exception:
            magn = None
        if not (magn is not None and evento.getAlcanceSismo() and evento.getOrigenGeneracion()):
            return {'success': False, 'error': 'Faltan datos obligatorios del evento', 'status_code': 400}
        
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

    def rechazarEventoSismico(self, evento: EventoSismico, usuario, estado_rechazado, fecha_hora, ult_cambio):
        evento.rechazar(estado_rechazado, fecha_hora, usuario, ult_cambio)

        db = SessionLocal()
        try:
            EventoRepository.from_domain(db, evento)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

        return True
        
    def confirmarEventoSismico(self, evento: EventoSismico, usuario, estado_aceptado, fecha_hora, ult_cambio):
        """
        Confirma un evento sísmico delegando en el dominio y persistiendo el cambio.
        Se mantiene la misma forma que `rechazarEventoSismico`: el método del gestor
        delega la lógica al dominio (`evento.confirmar`) y luego persiste usando
        `EventoRepository` dentro de una sesión.
        """
        # Delegar la confirmación al dominio; se espera que esto devuelva/actualice
        # el último cambio y pueda lanzar excepciones en caso de error.
        self.__ultimo_cambio = evento.confirmar(estado_aceptado, fecha_hora, usuario, ult_cambio)

        db = SessionLocal()
        try:
            EventoRepository.from_domain(db, evento)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

        return True

    def derivarEventoSismico(self, evento: EventoSismico, usuario, estado_derivado, fecha_hora, ult_cambio):
        """
        Deriva un evento sísmico a experto delegando en el dominio y persistiendo el cambio.
        Similar a confirmarEventoSismico y rechazarEventoSismico, delega la lógica al
        dominio (`evento.derivar`) y luego persiste usando EventoRepository.
        """
        self.__ultimo_cambio = evento.derivar(estado_derivado, fecha_hora, usuario, ult_cambio)

        db = SessionLocal()
        try:
            EventoRepository.from_domain(db, evento)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

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
            # Buscar el estado 'BloqueadoEnRevision' para bloquear el evento
            estado_bloqueado = self.buscarEstadoBloqueadoEnRevision(estados)
            usuario = self.buscarASLogueado(usuario_logueado)
            # Verificar que el usuario esté autorizado (empleado con rol administrador)
            if usuario is None:
                return {'success': False, 'error': 'Usuario no autorizado para bloquear eventos', 'status_code': 403}
            self._usuarioLogueado = usuario
            fec_hora = self.obtenerFechaHoraActual()
            if not estado_bloqueado:
                return {'success': False, 'error': 'Error al crear el estado bloqueado', 'status_code': 500}

            # Intentar bloquear el evento (cambiar su estado)
            if self.bloquearEventoSismico(evento_seleccionado, estado_bloqueado, fec_hora, usuario):
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
            self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)

            estado_rechazado = self.obtenerEstadoRechazado(estados)

            fec_hora = self.obtenerFechaHoraActual()
            
            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            self.rechazarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, estado_rechazado, fec_hora, self.__ultimo_cambio)
            return {'success': True, 'mensaje': 'Evento rechazado correctamente'}
        
        elif accion == 'conformar':
            self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)

            estado_conformado = self.obtenerEstadoConformado(estados)

            fec_hora = self.obtenerFechaHoraActual()
            
            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            self.confirmarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, estado_conformado, fec_hora, self.__ultimo_cambio)
            return {'success': True, 'mensaje': 'Evento confirmado correctamente'}
        
        elif accion == 'experto':
            self.validarDatosMinimosRequeridos(self.__eventoSismicoSeleccionado)

            estado_derivado = self.obtenerEstadoDerivado(estados)

            fec_hora = self.obtenerFechaHoraActual()
            
            # Pasar el Usuario logueado para que el Evento registre al Usuario responsable
            self.derivarEventoSismico(self.__eventoSismicoSeleccionado, self._usuarioLogueado, estado_derivado, fec_hora, self.__ultimo_cambio)
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
            except Exception:
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
        
        db = SessionLocal()
        try:
            EventoRepository.from_domain(db, evento)
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
            
        return {'success': True}
            





