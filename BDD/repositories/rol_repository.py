from typing import Optional
from sqlalchemy.orm import Session

from BDD import orm_models


class RolRepository:
    @staticmethod
    def get_or_create(db: Session, domain_rol) -> orm_models.Rol:
        """Busca un Rol por nombre, o lo crea si no existe."""
        nombre = domain_rol.getNombre()
        rol = db.query(orm_models.Rol).filter(orm_models.Rol.nombre == nombre).first()
        if rol:
            # actualizar descripción si cambió
            rol.descripcion = domain_rol.getDescripcion()
            return rol
        rol = orm_models.Rol(nombre=nombre, descripcion=domain_rol.getDescripcion())
        db.add(rol)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return rol

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Rol]:
        return db.query(orm_models.Rol).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Rol).all()

    @staticmethod
    def delete(db: Session, rol: orm_models.Rol):
        db.delete(rol)
