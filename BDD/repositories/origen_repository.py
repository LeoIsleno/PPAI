from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class OrigenRepository:
    @staticmethod
    def from_domain(db: Session, domain_origen) -> orm_models.OrigenDeGeneracion:
        nombre = domain_origen.getNombre()
        origen = db.query(orm_models.OrigenDeGeneracion).filter(orm_models.OrigenDeGeneracion.nombre == nombre).first()
        if origen:
            origen.descripcion = domain_origen.getDescripcion()
            return origen
        origen = orm_models.OrigenDeGeneracion(nombre=nombre, descripcion=domain_origen.getDescripcion())
        db.add(origen)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return origen

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.OrigenDeGeneracion]:
        return db.query(orm_models.OrigenDeGeneracion).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.OrigenDeGeneracion).all()

    @staticmethod
    def delete(db: Session, origen: orm_models.OrigenDeGeneracion):
        db.delete(origen)
