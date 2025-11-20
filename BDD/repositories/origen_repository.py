from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from .IBase_repository import IBaseRepository
from BACKEND.Modelos.OrigenDeGeneracion import OrigenDeGeneracion


class OrigenRepository(IBaseRepository):
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

    @staticmethod
    def to_domain(orm_origen):
        """
        Mapea un objeto ORM OrigenDeGeneracion a un objeto de dominio OrigenDeGeneracion.
        Este método es requerido por la interfaz BaseRepository.
        """
        if not orm_origen:
            return None
        
        # El mapeo convierte el objeto ORM a la entidad de dominio.
        return OrigenDeGeneracion(
            orm_origen.nombre, 
            orm_origen.descripcion
        )
