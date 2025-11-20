from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from BDD import orm_models
from BACKEND.Modelos.Estado import Estado
from .IBase_repository import IBaseRepository


class EstadoRepository(IBaseRepository):
    """Repository for Estado.

    Policy: this repository will attempt to resolve an Estado to an existing
    canonical row by `nombre`. If no canonical row exists, it will create
    and persist a new canonical `Estado` row using the normalized name returned
    by the domain factory. This reduces manual DB maintenance while still
    normalizing variants (e.g. "Auto-detectado" vs "AutoDetectado").
    """
    @staticmethod
    def from_domain(db: Session, estado):
        from BACKEND.Modelos.Estado import Estado as EstadoDom
        
        # 1. Obtener el nombre canónico del dominio (misma lógica que antes)
        raw_nombre = estado.getNombreEstado()
        canonical = EstadoDom.from_name(raw_nombre, estado.getAmbito())
        nombre_canonical = canonical.getNombreEstado()
        ambito_val = estado.getAmbito() # e.g. 'EventoSismico'

        # 2. Intentar encontrar el registro existente en la ÚNICA tabla
        existente = db.query(orm_models.Estado).filter_by(
            nombre=nombre_canonical.upper(),
            ambito=ambito_val
        ).first()
        
        if existente:
            return existente
        
        # 3. Si no existe, crear un nuevo registro en la tabla unificada
        try:
            nuevo = orm_models.Estado(nombre=nombre_canonical, ambito=ambito_val)
            db.add(nuevo)
            db.flush() # Para asignar el ID dentro de la transacción
            return nuevo
        except IntegrityError:
            # Esto maneja la rara condición de carrera donde otro proceso lo crea antes
            db.rollback()
            return db.query(orm_models.Estado).filter_by(nombre=nombre_canonical, ambito=ambito_val).first()

    @staticmethod
    def get_by_id(db: Session, id: int):
        """Busca un estado por ID en la tabla única 'estado'."""
        # Consulta: SELECT * FROM estado WHERE id = :id;
        return db.query(orm_models.Estado).get(id)

    @staticmethod
    def list_all(db: Session):
        """Obtiene todos los estados posibles desde la tabla única 'estado'."""
        # Consulta: SELECT * FROM estado;
        return db.query(orm_models.Estado).all()

    @staticmethod
    def delete(db: Session, estado):
        db.delete(estado)

    @staticmethod
    def to_domain(orm_estado: orm_models.Estado) -> Optional[Estado]:
        """
        CONTRATO CUMPLIDO: Mapea un objeto ORM de la tabla única 'estado' a 
        un objeto de dominio concreto (ej. EstadoAutoDetectado) usando el factory.
        """
        if not orm_estado:
            return None
            
        # El objeto ORM tiene 'nombre' y 'ambito'
        # El factory de dominio se encarga de instanciar la clase concreta correcta.
        return Estado.from_name(orm_estado.nombre, orm_estado.ambito)
