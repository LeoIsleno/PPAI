from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class CambioEstadoRepository:
    @staticmethod
    def from_domain(db: Session, cambio):
        from .estado_repository import EstadoRepository
        from .usuario_repository import UsuarioRepository
        
        nuevo = orm_models.CambioEstado(
            fecha_hora_inicio=cambio.getFechaHoraInicio(),
            fecha_hora_fin=cambio.getFechaHoraFin()
        )
        
        estado = cambio.getEstado()
        if estado:
            nuevo.estado = EstadoRepository.from_domain(db, estado)
            
        usuario = cambio.getUsuario()
        if usuario:
            nuevo.usuario = UsuarioRepository.from_domain(db, usuario)

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
