from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models

from .origen_repository import OrigenRepository
from .alcance_repository import AlcanceRepository
from .clasificacion_repository import ClasificacionRepository
from .estado_repository import EstadoRepository
from .cambio_estado_repository import CambioEstadoRepository
from .serie_repository import SerieRepository
from .magnitud_repository import MagnitudRepository

# Modelos de dominio
from BACKEND.Modelos.EventoSismico import EventoSismico
from BACKEND.Modelos.Estado import Estado
from BACKEND.Modelos.ClasificacionSismo import ClasificacionSismo
from BACKEND.Modelos.OrigenDeGeneracion import OrigenDeGeneracion
from BACKEND.Modelos.AlcanceSismo import AlcanceSismo
from BACKEND.Modelos.SerieTemporal import SerieTemporal
from BACKEND.Modelos.MuestraSismica import MuestraSismica
from BACKEND.Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from BACKEND.Modelos.TipoDeDato import TipoDeDato
from BACKEND.Modelos.CambioEstado import CambioEstado
from BACKEND.Modelos.Usuario import Usuario
from BACKEND.Modelos.MagnitudRichter import MagnitudRichter


class EventoRepository:
    @staticmethod
    def from_domain(db: Session, domain_evento) -> orm_models.EventoSismico:
        """Convierte un EventoSismico del dominio a EventoSismico ORM (campos básicos y relaciones directas)."""
        fecha = domain_evento.getFechaHoraOcurrencia()
        # Preferir el objeto MagnitudRichter si está presente en el dominio
        magn = None
        try:
            magn_obj = domain_evento.getMagnitud()
        except Exception:
            magn_obj = None

        if magn_obj is not None:
            try:
                magn = float(magn_obj.getNumero())
            except Exception:
                magn = None
        else:
            magn = None
        # Buscar evento existente por fecha y magnitud (si se dispone)
        evento = None
        try:
            if magn is not None:
                evento = db.query(orm_models.EventoSismico).join(orm_models.MagnitudRichter).filter(
                    orm_models.EventoSismico.fecha_hora_ocurrencia == fecha,
                    orm_models.MagnitudRichter.numero == magn
                ).first()
            else:
                evento = db.query(orm_models.EventoSismico).filter(
                    orm_models.EventoSismico.fecha_hora_ocurrencia == fecha
                ).first()
        except Exception:
            evento = db.query(orm_models.EventoSismico).filter(
                orm_models.EventoSismico.fecha_hora_ocurrencia == fecha
            ).first()
        if not evento:
            evento = orm_models.EventoSismico(
                fecha_hora_ocurrencia=fecha,
                fecha_hora_fin=domain_evento.getFechaHoraFin(),
                latitud_epicentro=domain_evento.getLatitudEpicentro(),
                longitud_epicentro=domain_evento.getLongitudEpicentro(),
                latitud_hipocentro=domain_evento.getLatitudHipocentro(),
                longitud_hipocentro=domain_evento.getLongitudHipocentro(),
            )
            db.add(evento)
            # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje

        origen_dom = domain_evento.getOrigenGeneracion()
        if origen_dom:
            evento.origen = OrigenRepository.from_domain(db, origen_dom)

        alcance_dom = domain_evento.getAlcanceSismo()
        if alcance_dom:
            evento.alcance = AlcanceRepository.from_domain(db, alcance_dom)

        clas_dom = domain_evento.getClasificacion()
        if clas_dom:
            evento.clasificacion = ClasificacionRepository.from_domain(db, clas_dom)

        estado_dom = domain_evento.getEstadoActual()
        if estado_dom:
            evento.estado_actual = EstadoRepository.from_domain(db, estado_dom)

        # Cambios de estado (si existen en el dominio) -> persistir y vincular
        cambios_dom = []
        try:
            cambios_dom = domain_evento.getCambiosEstado() or []
        except Exception:
            cambios_dom = []

        for cambio_dom in cambios_dom:
            # crear o mapear el cambio de estado y vincular al evento ORM
            cambio_orm = CambioEstadoRepository.from_domain(db, cambio_dom)
            cambio_orm.evento = evento
            # ensure it's present in evento.cambios_estado collection
            if cambio_orm not in evento.cambios_estado:
                evento.cambios_estado.append(cambio_orm)

        # Series temporales (si las hay en el dominio) -> persistir y vincular
        series_dom = []
        try:
            series_dom = domain_evento.getSerieTemporal() or []
        except Exception:
            series_dom = []

        for serie_dom in series_dom:
            serie_orm = SerieRepository.from_domain(db, serie_dom)
            serie_orm.evento = evento
            if serie_orm not in evento.serie_temporal:
                evento.serie_temporal.append(serie_orm)

        # Asociar/crear MagnitudRichter ORM si está disponible en el dominio o como número
        try:
            magn_dom = None
            try:
                magn_dom = domain_evento.getMagnitud()
            except Exception:
                magn_dom = None

            if magn_dom is not None:
                orm_magn = MagnitudRepository.from_domain(db, magn_dom)
                orm_magn.eventos.append(evento)
            elif magn is not None:
                # Construir un objeto de dominio MagnitudRichter a partir del número
                # y delegar siempre a from_domain para mantener consistencia
                try:
                    magn_dom_num = MagnitudRichter(None, magn)
                    orm_m = MagnitudRepository.from_domain(db, magn_dom_num)
                    if orm_m is not None:
                        # Vincular la magnitud ORM al evento
                        evento.magnitud = orm_m
                except Exception:
                    # si falla la construcción/consulta, no interrumpir el flujo
                    pass
        except Exception:
            # no interrumpir el flujo si falla la asociación de magnitud
            pass

        return evento

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.EventoSismico]:
        return db.query(orm_models.EventoSismico).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.EventoSismico).all()

    @staticmethod
    def delete(db: Session, evento: orm_models.EventoSismico):
        db.delete(evento)

    @staticmethod
    def to_domain(orm_event):
        """Mapea un EventoSismico ORM a la clase de dominio EventoSismico."""
        # Origen
        origen = None
        if orm_event.origen:
            origen = OrigenDeGeneracion(orm_event.origen.nombre, orm_event.origen.descripcion)

        # Alcance
        alcance = None
        if orm_event.alcance:
            alcance = AlcanceSismo(orm_event.alcance.descripcion, orm_event.alcance.nombre)

        # Clasificacion
        clas = None
        if orm_event.clasificacion:
            clas = ClasificacionSismo(orm_event.clasificacion.nombre,
                                      orm_event.clasificacion.km_profundidad_desde,
                                      orm_event.clasificacion.km_profundidad_hasta)

        # Estado actual
        estado = None
        if orm_event.estado_actual:
            estado = Estado.from_name(orm_event.estado_actual.nombre_estado, orm_event.estado_actual.ambito)

        # Cambios de estado
        cambios = []
        for ce in getattr(orm_event, 'cambios_estado', []):
            usuario_dom = None
            if ce.usuario:
                usuario_dom = Usuario(ce.usuario.nombre, getattr(ce.usuario, 'contrasena', ''), ce.usuario.fecha_alta, None)
            
            estado_ce = None
            if ce.estado:
                estado_ce = Estado.from_name(ce.estado.nombre_estado, ce.estado.ambito)
            
            cambios.append(CambioEstado(ce.fecha_hora_inicio, estado_ce, usuario_dom))

        # Series temporales
        series_dom = []
        for s in getattr(orm_event, 'serie_temporal', []):
            muestras_dom = []
            for m in getattr(s, 'muestras', []):
                detalles_dom = []
                for d in getattr(m, 'detalles', []):
                    tipo_dom = None
                    if d.tipo_de_dato:
                        tipo_dom = TipoDeDato(d.tipo_de_dato.denominacion,
                                            d.tipo_de_dato.nombre_unidad_medida,
                                            d.tipo_de_dato.valor_umbral)
                    detalles_dom.append(DetalleMuestraSismica(d.valor, tipo_dom))
                muestras_dom.append(MuestraSismica(m.fecha_hora_muestra, detalles_dom))

            estado_s = None
            if s.estado:
                estado_s = Estado.from_name(s.estado.nombre_estado, s.estado.ambito)

            serie_dom = SerieTemporal(s.fecha_hora_inicio_registro_muestras,
                                      s.fecha_hora_registro,
                                      s.frecuencia_muestreo,
                                      s.condicion_alarma,
                                      muestras_dom, # Pasamos la lista completa
                                      estado_s,
                                      []) # Asumo que el último parámetro es para algo que se llena después
            series_dom.append(serie_dom)

        # Preparar objeto MagnitudRichter de dominio si existe en ORM
        magn_dom_obj = None
        if getattr(orm_event, 'magnitud', None) is not None:
            try:
                magn_dom_obj = MagnitudRichter(orm_event.magnitud.descripcion, orm_event.magnitud.numero)
            except Exception:
                magn_dom_obj = None

        evento_dom = EventoSismico(
            fechaHoraOcurrencia=orm_event.fecha_hora_ocurrencia,
            latitudEpicentro=orm_event.latitud_epicentro,
            longitudEpicentro=orm_event.longitud_epicentro,
            latitudHipocentro=orm_event.latitud_hipocentro,
            longitudHipocentro=orm_event.longitud_hipocentro,
            magnitud=magn_dom_obj,
            origenGeneracion=origen,
            estadoActual=estado,
            cambiosEstado=cambios,
            clasificacion=clas,
            alcanceSismo=alcance,
            serieTemporal=series_dom
        )
        # magnitud ya asignada en el constructor cuando existía en ORM
        # Asignar campos adicionales después de la creación
        evento_dom.id_evento = orm_event.id
        if orm_event.fecha_hora_fin:
            evento_dom.setFechaHoraFin(orm_event.fecha_hora_fin)
        return evento_dom
