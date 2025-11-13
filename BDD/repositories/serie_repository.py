from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models


class SerieRepository:
    @staticmethod
    def from_domain(db: Session, serie):
        fecha_inicio = serie.getFechaHoraInicioRegistroMuestras()
        frecuencia = serie.getFrecuenciaMuestreo()
        
        existente = db.query(orm_models.SerieTemporal).filter(
            orm_models.SerieTemporal.fecha_hora_inicio_registro_muestras == fecha_inicio,
            orm_models.SerieTemporal.frecuencia_muestreo == frecuencia
        ).first()
        
        if existente:
            existente.fecha_hora_registro = serie.getFechaHoraRegistro()
            existente.condicion_alarma = serie.getCondicionAlarma()
            return existente

        nueva = orm_models.SerieTemporal(
            fecha_hora_inicio_registro_muestras=fecha_inicio,
            fecha_hora_registro=serie.getFechaHoraRegistro(),
            frecuencia_muestreo=frecuencia,
            condicion_alarma=serie.getCondicionAlarma()
        )
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
