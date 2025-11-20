from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class CambioEstadoRepository:
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
                if hasattr(estado_orm, 'nombre_estado'):
                    nuevo.estado_nombre = estado_orm.nombre_estado
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
