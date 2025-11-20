from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class AlcanceRepository:
    @staticmethod
    def from_domain(db: Session, alcance):
        nombre = alcance.getNombre()
        existente = db.query(orm_models.AlcanceSismo).filter_by(nombre=nombre).first()
        
        if existente:
            existente.descripcion = alcance.getDescripcion()
            return existente
            
        nuevo = orm_models.AlcanceSismo(
            nombre=nombre,
            descripcion=alcance.getDescripcion()
        )
        db.add(nuevo)
        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.AlcanceSismo]:
        return db.query(orm_models.AlcanceSismo).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.AlcanceSismo).all()

    @staticmethod
    def delete(db: Session, alcance: orm_models.AlcanceSismo):
        db.delete(alcance)
