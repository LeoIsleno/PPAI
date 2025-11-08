from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.MagnitudRichter import MagnitudRichter


class MagnitudRepository:
    @staticmethod
    def from_domain(db: Session, magnitud):
        if not magnitud:
            return None

        numero = magnitud.getNumero()
        descripcion = getattr(magnitud, 'getDescripcionMagnitud', lambda: None)()
        
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
