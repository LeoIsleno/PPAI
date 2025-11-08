from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class OrigenRepository:
    @staticmethod
    def from_domain(db: Session, origen):
        nombre = origen.getNombre()
        existente = db.query(orm_models.OrigenDeGeneracion).filter_by(nombre=nombre).first()
        
        if existente:
            existente.descripcion = origen.getDescripcion()
            return existente
            
        nuevo = orm_models.OrigenDeGeneracion(
            nombre=nombre,
            descripcion=origen.getDescripcion()
        )
        db.add(nuevo)
        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.OrigenDeGeneracion]:
        return db.query(orm_models.OrigenDeGeneracion).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.OrigenDeGeneracion).all()

    @staticmethod
    def delete(db: Session, origen: orm_models.OrigenDeGeneracion):
        db.delete(origen)
