from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.MagnitudRichter import MagnitudRichter
from typing import Optional
from .IBase_repository import IBaseRepository


class MagnitudRepository(IBaseRepository):
    @staticmethod
    def from_domain(db: Session, magnitud):
        if not magnitud:
            return None

        numero = magnitud.getNumero()
        descripcion = magnitud.getDescripcionMagnitud()

        if numero:
            existente = db.query(orm_models.MagnitudRichter).filter_by(numero=numero).first()
            if existente:
                return existente

        nueva = orm_models.MagnitudRichter(descripcion=descripcion, numero=numero)
        db.add(nueva)
        return nueva

    @staticmethod
    def to_domain(orm_magnitud):
        if not orm_magnitud:
            return None
        return MagnitudRichter(orm_magnitud.descripcion, orm_magnitud.numero)
    
    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.MagnitudRichter]:
        """Recupera un registro ORM por ID."""
        return db.query(orm_models.MagnitudRichter).get(id)

    @staticmethod
    def list_all(db: Session):
        """Lista todos los registros ORM de MagnitudRichter."""
        return db.query(orm_models.MagnitudRichter).all()

    @staticmethod
    def delete(db: Session, magnitud: orm_models.MagnitudRichter):
        """Elimina un registro ORM."""
        db.delete(magnitud)
