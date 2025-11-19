from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.Rol import Rol
from .IBase_repository import IBaseRepository


class RolRepository(IBaseRepository):
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

    @staticmethod
    def to_domain(orm_rol):
        if not orm_rol:
            return None
        return Rol(
            orm_rol.nombre,
            orm_rol.descripcion
        )
