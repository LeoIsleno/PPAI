from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class RolRepository:
    @staticmethod
    def get_or_create(db: Session, rol):
        nombre = rol.getNombre()
        existente = db.query(orm_models.Rol).filter_by(nombre=nombre).first()
        
        if existente:
            existente.descripcion = rol.getDescripcion()
            return existente
            
        nuevo = orm_models.Rol(
            nombre=nombre,
            descripcion=rol.getDescripcion()
        )
        db.add(nuevo)
        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Rol]:
        return db.query(orm_models.Rol).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Rol).all()

    @staticmethod
    def delete(db: Session, rol: orm_models.Rol):
        db.delete(rol)
