from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.SerieTemporal import SerieTemporal
from BACKEND.Modelos.Estado import Estado
from BACKEND.Modelos.MuestraSismica import MuestraSismica
from BACKEND.Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from BACKEND.Modelos.TipoDeDato import TipoDeDato
from .IBase_repository import IBaseRepository


class SerieRepository(IBaseRepository):
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
                    if hasattr(estado_orm, 'nombre'):
                        existente.estado_nombre = estado_orm.nombre
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
                if hasattr(estado_orm, 'nombre'):
                    nueva.estado_nombre = estado_orm.nombre
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

    @staticmethod
    def to_domain(orm_serie):
        """Mapea un objeto ORM SerieTemporal a un objeto de dominio SerieTemporal."""
        if not orm_serie:
            return None

        # 1. Mapear el estado (usa el cache de texto en ORM)
        estado_s = None
        if getattr(orm_serie, 'estado_nombre', None):
            estado_s = Estado.from_name(orm_serie.estado_nombre, orm_serie.estado_ambito)

        # 2. Mapear las muestras anidadas
        muestras = []
        for m in orm_serie.muestras or []:
            detalles = []
            for d in m.detalles or []:
                tipo = None
                if d.tipo_de_dato:
                    tipo = TipoDeDato(
                        d.tipo_de_dato.denominacion,
                        d.tipo_de_dato.nombre_unidad_medida,
                        d.tipo_de_dato.valor_umbral
                    )
                detalles.append(DetalleMuestraSismica(d.valor, tipo))
            muestras.append(MuestraSismica(m.fecha_hora_muestra, detalles))
            
        # 3. Crear el objeto de dominio SerieTemporal
        return SerieTemporal(
            orm_serie.fecha_hora_inicio_registro_muestras,
            orm_serie.fecha_hora_registro,
            orm_serie.frecuencia_muestreo,
            orm_serie.condicion_alarma,
            muestras, # Se pasan las muestras al constructor/setter
            estado_s,
            []
        )