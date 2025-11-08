from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class EstadoRepository:
    @staticmethod
    def from_domain(db: Session, estado):
        nombre = estado.getNombreEstado()
        existente = db.query(orm_models.Estado).filter_by(nombre_estado=nombre).first()
        
        if existente:
            existente.ambito = estado.getAmbito()
            return existente
            
        nuevo = orm_models.Estado(
            nombre_estado=nombre,
            ambito=estado.getAmbito()
        )
        db.add(nuevo)
        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Estado]:
        return db.query(orm_models.Estado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Estado).all()

    @staticmethod
    def delete(db: Session, estado: orm_models.Estado):
        db.delete(estado)
