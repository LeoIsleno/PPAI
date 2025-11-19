from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.CambioEstado import CambioEstado
from BACKEND.Modelos.Estado import Estado
from BACKEND.Modelos.Usuario import Usuario
from .IBase_repository import IBaseRepository


class CambioEstadoRepository(IBaseRepository):

    @staticmethod
    def from_domain(db: Session, cambio):
        from .estado_repository import EstadoRepository
        from .usuario_repository import UsuarioRepository
        # Intentar reutilizar un CambioEstado existente que tenga la misma
        # `fecha_hora_inicio` y coincida en estado/usuario. Esto reduce el
        # riesgo de colisiones entre eventos diferentes que casualmente
        # comparten la misma fecha.
        existente = None
        try:
            fecha_inicio = cambio.getFechaHoraInicio()
            estado_dom = cambio.getEstado()
            usuario_dom = cambio.getUsuario()

            estado_nombre = None
            if estado_dom and hasattr(estado_dom, 'getNombreEstado'):
                estado_nombre = estado_dom.getNombreEstado()

            usuario_nombre = None
            if usuario_dom and hasattr(usuario_dom, 'getNombre'):
                usuario_nombre = usuario_dom.getNombre()

            q = db.query(orm_models.CambioEstado).filter(orm_models.CambioEstado.fecha_hora_inicio == fecha_inicio)
            if estado_nombre:
                q = q.filter(orm_models.CambioEstado.estado_nombre == estado_nombre)
            if usuario_nombre:
                # join usuario to filter by usuario.nombre
                q = q.join(orm_models.Usuario).filter(orm_models.Usuario.nombre == usuario_nombre)

            existente = q.first()
        except Exception:
            existente = None

        if existente is None:
            nuevo = orm_models.CambioEstado(
                fecha_hora_inicio=cambio.getFechaHoraInicio(),
                fecha_hora_fin=cambio.getFechaHoraFin()
            )
        else:
            # Actualizar campos si ya existe
            nuevo = existente
            nuevo.fecha_hora_fin = cambio.getFechaHoraFin()
        
        estado = cambio.getEstado()
        if estado:
            estado_orm = EstadoRepository.from_domain(db, estado)
            if estado_orm:
                if hasattr(estado_orm, 'nombre'):
                    nuevo.estado_nombre = estado_orm.nombre
                if hasattr(estado_orm, 'ambito'):
                    nuevo.estado_ambito = estado_orm.ambito

        usuario = cambio.getUsuario()
        if usuario:
            nuevo.usuario = UsuarioRepository.from_domain(db, usuario)

        # Añadir sólo si es una nueva instancia ORM
        if existente is None:
            db.add(nuevo)

        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.CambioEstado]:
        return db.query(orm_models.CambioEstado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.CambioEstado).all()

    @staticmethod
    def delete(db: Session, cambio: orm_models.CambioEstado):
        db.delete(cambio)

    @staticmethod
    def to_domain(orm_cambio):
        """Mapea un objeto ORM CambioEstado a un objeto de dominio CambioEstado."""
        if not orm_cambio:
            return None

        # 1. Mapear el Usuario (solo datos básicos si no se carga la relación completa)
        usuario = None
        if orm_cambio.usuario:
            usuario = Usuario(
                orm_cambio.usuario.nombre,
                orm_cambio.usuario.contrasena,
                orm_cambio.usuario.fecha_alta,
                None # Empleado no se carga aquí para evitar recursión
            )

        # 2. Mapear el Estado (usa el cache de texto en ORM)
        estado_ce = None
        if getattr(orm_cambio, 'estado_nombre', None):
            estado_ce = Estado.from_name(orm_cambio.estado_nombre, orm_cambio.estado_ambito)
        
        # 3. Crear el objeto de dominio CambioEstado
        return CambioEstado(
            orm_cambio.fecha_hora_inicio,
            estado_ce,
            usuario,
            orm_cambio.fecha_hora_fin
        )
