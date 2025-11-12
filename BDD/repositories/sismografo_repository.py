from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from BACKEND.Modelos.Sismografo import Sismografo
from BACKEND.Modelos.EstacionSismologica import EstacionSismologica
from BACKEND.Modelos.SerieTemporal import SerieTemporal
from BACKEND.Modelos.MuestraSismica import MuestraSismica
from BACKEND.Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from BACKEND.Modelos.TipoDeDato import TipoDeDato
from BACKEND.Modelos.Estado import Estado


class SismografoRepository:
    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Sismografo).all()

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Sismografo]:
        return db.query(orm_models.Sismografo).get(id)

    @staticmethod
    def to_domain(orm_sismografo):
        estacion = None
        if orm_sismografo.estacion:
            est = orm_sismografo.estacion
            estacion = EstacionSismologica(
                codigoEstacion=est.codigo_estacion,
                nombre=est.nombre,
                latitud=est.latitud,
                longitud=est.longitud,
                documentoCertificacionAdq=est.documento_certificacion_adq,
                fechaSolicitudCertificacion=est.fecha_solicitud_certificacion,
                nroCertificacionAdquisicion=est.nro_certificacion_adquisicion
            )

        series = []
        for s in orm_sismografo.series_temporales or []:
            muestras = []
            for m in s.muestras or []:
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

            estado = None
            estado_nombre = getattr(s, 'estado_nombre', None)
            estado_ambito = getattr(s, 'estado_ambito', None)
            if estado_nombre:
                estado = Estado.from_name(estado_nombre, estado_ambito)

            serie = SerieTemporal(
                s.fecha_hora_inicio_registro_muestras,
                s.fecha_hora_registro,
                s.frecuencia_muestreo,
                s.condicion_alarma,
                muestras[0] if muestras else None,
                estado,
                []
            )
            for muestra in muestras[1:]:
                serie.agregarMuestraSismica(muestra)
            series.append(serie)

        return Sismografo(
            identificadorSismografo=orm_sismografo.identificador_sismografo,
            nroSerie=orm_sismografo.nro_serie,
            fechaAdquisicion=orm_sismografo.fecha_adquisicion,
            estacionSismologica=estacion,
            serieTemporal=series,
            estado=None,
            cambiosEstado=[]
        )
