from typing import Optional
from sqlalchemy.orm import Session

from BDD import orm_models


class CambioEstadoRepository:
    @staticmethod
    def from_domain(db: Session, domain_cambio) -> orm_models.CambioEstado:
        # construir CambioEstado ORM a partir del dominio
        fecha_inicio = domain_cambio.getFechaHoraInicio()
        fecha_fin = domain_cambio.getFechaHoraFin()
        estado_dom = domain_cambio.getEstado()
        usuario_dom = domain_cambio.getUsuario()

        # buscar por unicidad relativa: fechaInicio + evento_id no está en dominio, asumimos creación
        ce = orm_models.CambioEstado(
            fecha_hora_inicio=fecha_inicio,
            fecha_hora_fin=fecha_fin,
        )
        # relaciones: estado/usuario deben ser creados por sus repositorios antes
        if estado_dom:
            from .estado_repository import EstadoRepository
            ce.estado = EstadoRepository.from_domain(db, estado_dom)
        if usuario_dom:
            from .usuario_repository import UsuarioRepository
            ce.usuario = UsuarioRepository.from_domain(db, usuario_dom)

        db.add(ce)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return ce

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.CambioEstado]:
        return db.query(orm_models.CambioEstado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.CambioEstado).all()

    @staticmethod
    def delete(db: Session, cambio: orm_models.CambioEstado):
        db.delete(cambio)
