from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class AlcanceRepository:
    @staticmethod
    def from_domain(db: Session, domain_alcance) -> orm_models.AlcanceSismo:
        nombre = domain_alcance.getNombre()
        alcance = db.query(orm_models.AlcanceSismo).filter(orm_models.AlcanceSismo.nombre == nombre).first()
        if alcance:
            alcance.descripcion = domain_alcance.getDescripcion()
            return alcance
        alcance = orm_models.AlcanceSismo(nombre=nombre, descripcion=domain_alcance.getDescripcion())
        db.add(alcance)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return alcance

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.AlcanceSismo]:
        return db.query(orm_models.AlcanceSismo).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.AlcanceSismo).all()

    @staticmethod
    def delete(db: Session, alcance: orm_models.AlcanceSismo):
        db.delete(alcance)
