from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class EstadoRepository:
    """Repository for Estado.

    Important policy: this repository will NOT create new Estado rows automatically.
    The canonical Estado rows must exist in the database (see `BDD/seed_states.py`).
    Any attempt to persist a non-canonical Estado will raise a RuntimeError so the
    caller can handle it explicitly. This prevents accidental proliferation of
    duplicate Estado rows.
    """
    @staticmethod
    def from_domain(db: Session, estado):
        # Normalize the state name using the Estado factory so we store a canonical
        # representation in the DB. This avoids creating duplicate Estado rows when
        # different spellings/variants are used (e.g. "Auto-detectado" vs "AutoDetectado"
        # or "Bloqueado en Revisión" vs "BloqueadoEnRevision").
        try:
            from BACKEND.Modelos.Estado import Estado as EstadoDom
            raw_nombre = estado.getNombreEstado() if hasattr(estado, 'getNombreEstado') else str(estado)
            # Use the Estado.from_name factory to obtain a canonical instance
            canonical = EstadoDom.from_name(raw_nombre, estado.getAmbito() if hasattr(estado, 'getAmbito') else None)
            nombre_canonical = canonical.getNombreEstado()
        except Exception:
            # Fallback: use the raw name if anything goes wrong
            nombre_canonical = estado.getNombreEstado() if hasattr(estado, 'getNombreEstado') else str(estado)

        # Try to find an existing Estado by the canonical name
        existente = db.query(orm_models.Estado).filter_by(nombre_estado=nombre_canonical).first()

        if existente:
            existente.ambito = estado.getAmbito()
            return existente

        # IMPORTANT: do not create new Estado rows automatically.
        # The application must use the existing states defined in the DB.
        # If a canonical match is not found, raise so the caller can decide
        # how to handle the missing state (avoid silently creating duplicates).
        raise RuntimeError(f"Estado '{nombre_canonical}' no encontrado en la base de datos. No se crearán nuevos estados automáticamente.")

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Estado]:
        return db.query(orm_models.Estado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Estado).all()

    @staticmethod
    def delete(db: Session, estado: orm_models.Estado):
        db.delete(estado)
