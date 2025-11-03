from typing import Optional
from sqlalchemy.orm import Session

from BDD import orm_models


class SerieRepository:
    @staticmethod
    def from_domain(db: Session, domain_serie) -> orm_models.SerieTemporal:
        fecha_inicio = domain_serie.getFechaHoraInicioRegistroMuestras()
        fecha_reg = domain_serie.getFechaHoraRegistro()
        freq = domain_serie.getFrecuenciaMuestreo()
        condicion = domain_serie.getCondicionAlarma()

        serie = db.query(orm_models.SerieTemporal).filter(
            orm_models.SerieTemporal.fecha_hora_inicio_registro_muestras == fecha_inicio,
            orm_models.SerieTemporal.frecuencia_muestreo == freq,
        ).first()
        if serie:
            serie.fecha_hora_registro = fecha_reg
            serie.condicion_alarma = condicion
            return serie

        serie = orm_models.SerieTemporal(
            fecha_hora_inicio_registro_muestras=fecha_inicio,
            fecha_hora_registro=fecha_reg,
            frecuencia_muestreo=freq,
            condicion_alarma=condicion,
        )
        db.add(serie)
        # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje
        return serie

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.SerieTemporal]:
        return db.query(orm_models.SerieTemporal).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.SerieTemporal).all()

    @staticmethod
    def delete(db: Session, serie: orm_models.SerieTemporal):
        db.delete(serie)
