from typing import Optional
from sqlalchemy.orm import Session, joinedload
from BDD import orm_models
from .origen_repository import OrigenRepository
from .alcance_repository import AlcanceRepository
from .clasificacion_repository import ClasificacionRepository
from .estado_repository import EstadoRepository
from .cambio_estado_repository import CambioEstadoRepository
from .serie_repository import SerieRepository
from .magnitud_repository import MagnitudRepository
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
from .IBase_repository import IBaseRepository


class EventoRepository(IBaseRepository):
    @staticmethod
    def from_domain(db: Session, evento):

        # 1. INTENTAR BUSCAR POR ID PRIMERO (Esta es la corrección clave)
        existente = None
        if evento.getId(): # Si el objeto de dominio ya tiene un ID cargado
            existente = db.query(orm_models.EventoSismico).get(evento.getId())

        # 2. Fallback: Buscar por fecha (solo si es un evento nuevo sin ID)
        if not existente:
            fecha = evento.getFechaHoraOcurrencia()
            existente = db.query(orm_models.EventoSismico).filter_by(fecha_hora_ocurrencia=fecha).first()
        
        # 3. Crear nuevo si no existe
        if not existente:
            existente = orm_models.EventoSismico()
            db.add(existente)

        # 4. ACTUALIZAR TODOS LOS CAMPOS (Importante para "Modificar Datos")
        # Siempre actualizamos los campos escalares por si cambiaron en el Gestor
        existente.fecha_hora_ocurrencia = evento.getFechaHoraOcurrencia()
        existente.fecha_hora_fin = evento.getFechaHoraFin()
        existente.latitud_epicentro = evento.getLatitudEpicentro()
        existente.longitud_epicentro = evento.getLongitudEpicentro()
        existente.latitud_hipocentro = evento.getLatitudHipocentro()
        existente.longitud_hipocentro = evento.getLongitudHipocentro()

        # 5. Actualizar Estado (Usando columnas de texto como definimos)
        estado = evento.getEstadoActual()
        if estado:
            # Usamos el repo de estado para asegurar persistencia/mapeo, pero guardamos texto
            estado_orm = EstadoRepository.from_domain(db, estado)
            if estado_orm:
                existente.estado_actual_nombre = estado_orm.nombre
                existente.estado_actual_ambito = estado_orm.ambito

        # 6. Actualizar Magnitud (Lógica corregida)
        magnitud_obj = evento.getMagnitud()
        if magnitud_obj:
            # Usar el repositorio de magnitud para buscar o crear
            mag_orm = MagnitudRepository.from_domain(db, magnitud_obj)
            existente.magnitud = mag_orm 

        # 7. Actualizar otras relaciones (Origen, Alcance, Clasificación)
        origen = evento.getOrigenGeneracion()
        if origen:
            existente.origen = OrigenRepository.from_domain(db, origen)

        alcance = evento.getAlcanceSismo()
        if alcance:
            existente.alcance = AlcanceRepository.from_domain(db, alcance)

        clasificacion = evento.getClasificacion()
        if clasificacion:
            existente.clasificacion = ClasificacionRepository.from_domain(db, clasificacion)

        # 8. Actualizar Cambios de Estado (Append solo los nuevos)
        cambios = evento.getCambiosEstado() or []
        for cambio in cambios:
            # Si el cambio ya tiene ID o ya está en la lista, se gestiona en from_domain
            cambio_orm = CambioEstadoRepository.from_domain(db, cambio)
            if cambio_orm not in existente.cambios_estado:
                existente.cambios_estado.append(cambio_orm)
                # Importante: Vincular el cambio al evento actual
                cambio_orm.evento = existente 

        # Nota: Las Series Temporales suelen ser pesadas, verifica si necesitas actualizarlas
        # en cada guardado del evento o si se manejan aparte.

        return existente

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.EventoSismico]:
        return db.query(orm_models.EventoSismico).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.EventoSismico).options(
            # Cargar Series Temporales (relación 1)
            joinedload(orm_models.EventoSismico.serie_temporal) 
                # Cargar el Sismografo dentro de cada Serie (relación 2)
                .joinedload(orm_models.SerieTemporal.sismografo) 
                # Cargar la Estacion dentro del Sismografo (relación 3)
                .joinedload(orm_models.Sismografo.estacion)
        ).all()

    @staticmethod
    def delete(db: Session, evento: orm_models.EventoSismico):
        db.delete(evento)

    @staticmethod
    def to_domain(orm_evento):
        origen = None
        if orm_evento.origen:
            origen = OrigenDeGeneracion(
                orm_evento.origen.nombre,
                orm_evento.origen.descripcion
            )

        alcance = None
        if orm_evento.alcance:
            alcance = AlcanceSismo(
                orm_evento.alcance.descripcion,
                orm_evento.alcance.nombre
            )

        clasificacion = None
        if orm_evento.clasificacion:
            c = orm_evento.clasificacion
            clasificacion = ClasificacionSismo(
                c.nombre,
                c.km_profundidad_desde,
                c.km_profundidad_hasta
            )

        estado = None
        # Resolve estado from cached columns (preferred)
        if getattr(orm_evento, 'estado_actual_nombre', None):
            estado = Estado.from_name(
                orm_evento.estado_actual_nombre,
                orm_evento.estado_actual_ambito
            )
        
        cambios = []
        for ce in orm_evento.cambios_estado or []:
            usuario = None
            if ce.usuario:
                usuario = Usuario(
                    ce.usuario.nombre,
                    ce.usuario.contrasena,
                    ce.usuario.fecha_alta,
                    None
                )
            
            estado_ce = None
            # Prefer cached values on CambioEstado
            if getattr(ce, 'estado_nombre', None):
                estado_ce = Estado.from_name(ce.estado_nombre, ce.estado_ambito)
            
            cambios.append(CambioEstado(ce.fecha_hora_inicio, estado_ce, usuario))

        series = []
        for s in orm_evento.serie_temporal or []:
            muestras = []
            for m in s.muestras or []:
                detalles = []
                for d in m.detalles or []:
                    tipo = None
                    if d.tipo_de_dato:
                        tipo = TipoDeDato(
                            d.tipo_de_dato.denominacion,
                            d.tipo_de_dato.nombre_unidad_medida,
                            d.tipo_de_dato.valor_umbral
                        )
                    detalles.append(DetalleMuestraSismica(d.valor, tipo))
                muestras.append(MuestraSismica(m.fecha_hora_muestra, detalles))

            estado_s = None
            # Prefer cached nombre/ambito on SerieTemporal
            if getattr(s, 'estado_nombre', None):
                estado_s = Estado.from_name(s.estado_nombre, s.estado_ambito)

            serie = SerieTemporal(
                s.fecha_hora_inicio_registro_muestras,
                s.fecha_hora_registro,
                s.frecuencia_muestreo,
                s.condicion_alarma,
                muestras,
                estado_s,
                []
            )
            series.append(serie)

        magnitud = None
        if orm_evento.magnitud:
            magnitud = MagnitudRichter(
                orm_evento.magnitud.descripcion,
                orm_evento.magnitud.numero
            )

        evento = EventoSismico(
            fechaHoraOcurrencia=orm_evento.fecha_hora_ocurrencia,
            latitudEpicentro=orm_evento.latitud_epicentro,
            longitudEpicentro=orm_evento.longitud_epicentro,
            latitudHipocentro=orm_evento.latitud_hipocentro,
            longitudHipocentro=orm_evento.longitud_hipocentro,
            magnitud=magnitud,
            origenGeneracion=origen,
            estadoActual=estado,
            cambiosEstado=cambios,
            clasificacion=clasificacion,
            alcanceSismo=alcance,
            serieTemporal=series
        )
        
        evento.setId(orm_evento.id)
        if orm_evento.fecha_hora_fin:
            evento.setFechaHoraFin(orm_evento.fecha_hora_fin)
            
        return evento
