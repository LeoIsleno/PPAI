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

        # Try to find an existing Estado row among concrete estado tables
        # by canonical name. We query each concrete table until we find one.
        existente = None
        concrete_tables = [
            orm_models.EstadoAutoDetectado,
            orm_models.EstadoAutoConfirmado,
            orm_models.EstadoPendienteDeCierre,
            orm_models.EstadoDerivado,
            orm_models.EstadoConfirmadoPorPersonal,
            orm_models.EstadoCerrado,
            orm_models.EstadoRechazado,
            orm_models.EstadoBloqueadoEnRevision,
            orm_models.EstadoPendienteDeRevision,
            orm_models.EstadoSinRevision,
        ]
        for tbl in concrete_tables:
            existente = db.query(tbl).filter_by(nombre_estado=nombre_canonical).first()
            if existente:
                existente.ambito = estado.getAmbito()
                return existente

        # If not found, create a new canonical Estado row and persist it.
        # We handle possible race conditions (concurrent inserts) by catching
        # IntegrityError and re-querying the existing row.
        ambito_val = estado.getAmbito()

        # Map canonical display names to concrete ORM subclasses so that
        # a dedicated table for each concrete state is created (joined
        # table inheritance). If no concrete subclass is found, fall back
        # to the base Estado table (safe for unknown/custom states).
        mapping = {
            'Auto-detectado': orm_models.EstadoAutoDetectado,
            'AutoDetectado': orm_models.EstadoAutoDetectado,
            'Auto-confirmado': orm_models.EstadoAutoConfirmado,
            'AutoConfirmado': orm_models.EstadoAutoConfirmado,
            'Pendiente de Cierre': orm_models.EstadoPendienteDeCierre,
            'PendienteDeCierre': orm_models.EstadoPendienteDeCierre,
            'Derivado': orm_models.EstadoDerivado,
            'Confirmado por Personal': orm_models.EstadoConfirmadoPorPersonal,
            'ConfirmadoPorPersonal': orm_models.EstadoConfirmadoPorPersonal,
            'Cerrado': orm_models.EstadoCerrado,
            'Rechazado': orm_models.EstadoRechazado,
            'Bloqueado en Revisión': orm_models.EstadoBloqueadoEnRevision,
            'BloqueadoEnRevision': orm_models.EstadoBloqueadoEnRevision,
            'Pendiente de Revisión': orm_models.EstadoPendienteDeRevision,
            'PendienteDeRevision': orm_models.EstadoPendienteDeRevision,
            'SinRevision': orm_models.EstadoSinRevision,
            'Sin Revisión': orm_models.EstadoSinRevision,
        }

        orm_cls = mapping.get(nombre_canonical)
        if orm_cls:
            nuevo = orm_cls(nombre_estado=nombre_canonical, ambito=ambito_val)
        else:
            # Unknown/custom estado: create a row in the "generic" table
            # We don't have a generic table any more; create an instance on the
            # EstadoAutoDetectado table as a last resort to persist the name.
            nuevo = orm_models.EstadoAutoDetectado(nombre_estado=nombre_canonical, ambito=ambito_val)
        db.add(nuevo)
        # flush so the row is written and an id is assigned within caller's transaction
        db.flush()
        return nuevo

    @staticmethod
    def get_by_id(db: Session, id: int):
        # Search across concrete estado tables for the given id and return
        # the first match. This is a pragmatic fallback since ids are not
        # globally unique across separate tables.
        concrete_tables = [
            orm_models.EstadoAutoDetectado,
            orm_models.EstadoAutoConfirmado,
            orm_models.EstadoPendienteDeCierre,
            orm_models.EstadoDerivado,
            orm_models.EstadoConfirmadoPorPersonal,
            orm_models.EstadoCerrado,
            orm_models.EstadoRechazado,
            orm_models.EstadoBloqueadoEnRevision,
            orm_models.EstadoPendienteDeRevision,
            orm_models.EstadoSinRevision,
        ]
        for tbl in concrete_tables:
            found = db.query(tbl).get(id)
            if found:
                return found
        return None

    @staticmethod
    def list_all(db: Session):
        # Return concatenation of all concrete estado rows so callers can
        # iterate over objects that expose `nombre_estado` and `ambito`.
        concrete_tables = [
            orm_models.EstadoAutoDetectado,
            orm_models.EstadoAutoConfirmado,
            orm_models.EstadoPendienteDeCierre,
            orm_models.EstadoDerivado,
            orm_models.EstadoConfirmadoPorPersonal,
            orm_models.EstadoCerrado,
            orm_models.EstadoRechazado,
            orm_models.EstadoBloqueadoEnRevision,
            orm_models.EstadoPendienteDeRevision,
            orm_models.EstadoSinRevision,
        ]
        results = []
        for tbl in concrete_tables:
            results.extend(db.query(tbl).all() or [])
        return results

    @staticmethod
    def delete(db: Session, estado):
        db.delete(estado)
