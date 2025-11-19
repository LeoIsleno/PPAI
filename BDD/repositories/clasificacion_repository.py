from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.ClasificacionSismo import ClasificacionSismo
from .IBase_repository import IBaseRepository


class ClasificacionRepository(IBaseRepository):
    @staticmethod
    def from_domain(db: Session, clasificacion):
        nombre = clasificacion.getNombre()
        resultado = db.query(orm_models.ClasificacionSismo).filter_by(nombre=nombre).first()
        
        if resultado:
            resultado.km_profundidad_desde = clasificacion.getKmProfundidadDesde()
            resultado.km_profundidad_hasta = clasificacion.getKmProfundidadHasta()
            return resultado
            
        nueva = orm_models.ClasificacionSismo(
            nombre=nombre,
            km_profundidad_desde=clasificacion.getKmProfundidadDesde(),
            km_profundidad_hasta=clasificacion.getKmProfundidadHasta()
        )
        db.add(nueva)
        return nueva

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.ClasificacionSismo]:
        return db.query(orm_models.ClasificacionSismo).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.ClasificacionSismo).all()

    @staticmethod
    def delete(db: Session, clasificacion: orm_models.ClasificacionSismo):
        db.delete(clasificacion)

    @staticmethod
    def to_domain(orm_clasificacion):
        """
        Mapea un objeto ORM ClasificacionSismo a un objeto de dominio ClasificacionSismo.
        Este método es requerido por la interfaz BaseRepository.
        """
        if not orm_clasificacion:
            return None
        
        # El mapeo convierte el objeto ORM a la entidad de dominio.
        return ClasificacionSismo(
            orm_clasificacion.nombre, 
            orm_clasificacion.km_profundidad_desde,
            orm_clasificacion.km_profundidad_hasta
        )
