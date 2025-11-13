from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class SerieRepository:
    @staticmethod
    def from_domain(db: Session, serie):
        from .estado_repository import EstadoRepository
        
        fecha_inicio = serie.getFechaHoraInicioRegistroMuestras()
        frecuencia = serie.getFrecuenciaMuestreo()
        
        existente = db.query(orm_models.SerieTemporal).filter(
            orm_models.SerieTemporal.fecha_hora_inicio_registro_muestras == fecha_inicio,
            orm_models.SerieTemporal.frecuencia_muestreo == frecuencia
        ).first()
        
        if existente:
            existente.fecha_hora_registro = serie.getFechaHoraRegistro()
            existente.condicion_alarma = serie.getCondicionAlarma()
            
            # Actualizar estado si existe (solo cache; no relación a tabla base)
            estado = serie.getEstado()
            if estado:
                estado_orm = EstadoRepository.from_domain(db, estado)
                if estado_orm:
                    if hasattr(estado_orm, 'nombre_estado'):
                        existente.estado_nombre = estado_orm.nombre_estado
                    if hasattr(estado_orm, 'ambito'):
                        existente.estado_ambito = estado_orm.ambito
            return existente

        nueva = orm_models.SerieTemporal(
            fecha_hora_inicio_registro_muestras=fecha_inicio,
            fecha_hora_registro=serie.getFechaHoraRegistro(),
            frecuencia_muestreo=frecuencia,
            condicion_alarma=serie.getCondicionAlarma()
        )
        
        # Agregar estado si existe (solo cache)
        estado = serie.getEstado()
        if estado:
            estado_orm = EstadoRepository.from_domain(db, estado)
            if estado_orm:
                if hasattr(estado_orm, 'nombre_estado'):
                    nueva.estado_nombre = estado_orm.nombre_estado
                if hasattr(estado_orm, 'ambito'):
                    nueva.estado_ambito = estado_orm.ambito
        
        db.add(nueva)
        return nueva

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.SerieTemporal]:
        return db.query(orm_models.SerieTemporal).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.SerieTemporal).all()

    @staticmethod
    def delete(db: Session, serie: orm_models.SerieTemporal):
        db.delete(serie)
