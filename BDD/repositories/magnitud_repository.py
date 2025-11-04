from sqlalchemy.orm import Session
from BDD import orm_models

from BACKEND.Modelos.MagnitudRichter import MagnitudRichter


class MagnitudRepository:
    @staticmethod
    def from_domain(db: Session, domain_magnitud: MagnitudRichter) -> orm_models.MagnitudRichter:
        """Mapea MagnitudRichter dominio a ORM y la añade a la sesión si no existe."""
        if domain_magnitud is None:
            return None

        # Intentar encontrar por numero y descripcion
        numero = None
        try:
            numero = float(domain_magnitud.getNumero())
        except Exception:
            numero = None

        descripcion = domain_magnitud.getDescripcionMagnitud() if hasattr(domain_magnitud, 'getDescripcionMagnitud') else None

        query = db.query(orm_models.MagnitudRichter)
        if numero is not None:
            existing = query.filter(orm_models.MagnitudRichter.numero == numero).first()
            if existing:
                return existing

        # Crear nueva entidad ORM
        orm_m = orm_models.MagnitudRichter(descripcion=descripcion, numero=numero)
        db.add(orm_m)
        # dejar que el commit del caller haga flush/commit
        return orm_m

    @staticmethod
    def to_domain(orm_magnitud: orm_models.MagnitudRichter):
        if orm_magnitud is None:
            return None
        return MagnitudRichter(orm_magnitud.descripcion, orm_magnitud.numero)
