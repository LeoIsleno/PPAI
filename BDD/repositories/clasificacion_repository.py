from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class ClasificacionRepository:
    @staticmethod
    def from_domain(db: Session, domain_clas) -> orm_models.ClasificacionSismo:
        nombre = domain_clas.getNombre()
        clas = db.query(orm_models.ClasificacionSismo).filter(orm_models.ClasificacionSismo.nombre == nombre).first()
        if clas:
            clas.km_profundidad_desde = domain_clas.getKmProfundidadDesde()
            clas.km_profundidad_hasta = domain_clas.getKmProfundidadHasta()
            return clas
        clas = orm_models.ClasificacionSismo(
            nombre=nombre,
            km_profundidad_desde=domain_clas.getKmProfundidadDesde(),
            km_profundidad_hasta=domain_clas.getKmProfundidadHasta(),
        )
        db.add(clas)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return clas

        @staticmethod
        def get_by_id(db: Session, id: int) -> Optional[orm_models.ClasificacionSismo]:
            return db.query(orm_models.ClasificacionSismo).get(id)

        @staticmethod
        def list_all(db: Session):
            return db.query(orm_models.ClasificacionSismo).all()

        @staticmethod
        def delete(db: Session, clas: orm_models.ClasificacionSismo):
            db.delete(clas)
