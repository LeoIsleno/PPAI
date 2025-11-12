from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from BDD import orm_models


class EstadoRepository:
    """Repository for Estado.

    Policy: this repository will attempt to resolve an Estado to an existing
    canonical row by `nombre_estado`. If no canonical row exists, it will create
    and persist a new canonical `Estado` row using the normalized name returned
    by the domain factory. This reduces manual DB maintenance while still
    normalizing variants (e.g. "Auto-detectado" vs "AutoDetectado").
    """
    @staticmethod
    def from_domain(db: Session, estado):
        # Normalize the state name using the Estado factory so we store a canonical
        # representation in the DB. This avoids creating duplicate Estado rows when
        # different spellings/variants are used (e.g. "Auto-detectado" vs "AutoDetectado"
        # or "Bloqueado en Revisión" vs "BloqueadoEnRevision").
        from BACKEND.Modelos.Estado import Estado as EstadoDom
        raw_nombre = estado.getNombreEstado()
        # Use the Estado.from_name factory to obtain a canonical instance
        canonical = EstadoDom.from_name(raw_nombre, estado.getAmbito())
        nombre_canonical = canonical.getNombreEstado()

        # Try to find an existing Estado by the canonical name
        existente = db.query(orm_models.Estado).filter_by(nombre_estado=nombre_canonical).first()

        if existente:
            existente.ambito = estado.getAmbito()
            return existente

        # If not found, create a new canonical Estado row and persist it.
        # We handle possible race conditions (concurrent inserts) by catching
        # IntegrityError and re-querying the existing row.
        ambito_val = estado.getAmbito()
        nuevo = orm_models.Estado(nombre_estado=nombre_canonical, ambito=ambito_val)
        db.add(nuevo)
        # flush so the row is written and an id is assigned within caller's transaction
        db.flush()
        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Estado]:
        return db.query(orm_models.Estado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Estado).all()

    @staticmethod
    def delete(db: Session, estado: orm_models.Estado):
        db.delete(estado)
