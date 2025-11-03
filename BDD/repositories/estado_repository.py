from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class EstadoRepository:
    @staticmethod
    def from_domain(db: Session, domain_estado) -> orm_models.Estado:
        nombre = domain_estado.getNombreEstado()
        estado = db.query(orm_models.Estado).filter(orm_models.Estado.nombre_estado == nombre).first()
        if estado:
            estado.ambito = domain_estado.getAmbito()
            return estado
        estado = orm_models.Estado(nombre_estado=nombre, ambito=domain_estado.getAmbito())
        db.add(estado)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return estado

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Estado]:
        return db.query(orm_models.Estado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Estado).all()

    @staticmethod
    def delete(db: Session, estado: orm_models.Estado):
        db.delete(estado)
