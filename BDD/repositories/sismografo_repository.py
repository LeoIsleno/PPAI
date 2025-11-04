from typing import Optional
from sqlalchemy.orm import Session

from BDD import orm_models


class SismografoRepository:
    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Sismografo).all()

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Sismografo]:
        return db.query(orm_models.Sismografo).get(id)

    @staticmethod
    def to_domain(orm_s):
        # mapping to domain Sismografo
        from BACKEND.Modelos.Sismografo import Sismografo
        from BACKEND.Modelos.EstacionSismologica import EstacionSismologica
        from BACKEND.Modelos.SerieTemporal import SerieTemporal
        from BACKEND.Modelos.MuestraSismica import MuestraSismica
        from BACKEND.Modelos.DetalleMuestraSismica import DetalleMuestraSismica
        from BACKEND.Modelos.TipoDeDato import TipoDeDato
        from BACKEND.Modelos.Estado import Estado

        estacion_dom = None
        if orm_s.estacion:
            estacion = orm_s.estacion
            estacion_dom = EstacionSismologica(
                codigoEstacion=estacion.codigo_estacion,
                nombre=estacion.nombre,
                latitud=estacion.latitud,
                longitud=estacion.longitud,
                documentoCertificacionAdq=estacion.documento_certificacion_adq,
                fechaSolicitudCertificacion=estacion.fecha_solicitud_certificacion,
                nroCertificacionAdquisicion=estacion.nro_certificacion_adquisicion
            )

        series_dom = []
        for s in getattr(orm_s, 'series_temporales', []) or []:
            muestras_dom = []
            for m in getattr(s, 'muestras', []) or []:
                detalles_dom = []
                for d in getattr(m, 'detalles', []) or []:
                    tipo_dom = TipoDeDato(d.tipo_de_dato.denominacion if d.tipo_de_dato else None,
                                            d.tipo_de_dato.nombre_unidad_medida if d.tipo_de_dato else None,
                                            d.tipo_de_dato.valor_umbral if d.tipo_de_dato else None)
                    detalles_dom.append(DetalleMuestraSismica(d.valor, tipo_dom))
                muestras_dom.append(MuestraSismica(m.fecha_hora_muestra, detalles_dom))

            estado_s = None
            if s.estado:
                estado_s = Estado.from_name(s.estado.nombre_estado, s.estado.ambito)

            serie_dom = SerieTemporal(s.fecha_hora_inicio_registro_muestras,
                                      s.fecha_hora_registro,
                                      s.frecuencia_muestreo,
                                      s.condicion_alarma,
                                      muestras_dom[0] if muestras_dom else None,
                                      estado_s,
                                      [])
            for mm in muestras_dom[1:]:
                serie_dom.agregarMuestraSismica(mm)
            series_dom.append(serie_dom)

        sismograf_dom = Sismografo(
            identificadorSismografo=orm_s.identificador_sismografo,
            nroSerie=orm_s.nro_serie,
            fechaAdquisicion=orm_s.fecha_adquisicion,
            estacionSismologica=estacion_dom,
            serieTemporal=series_dom,
            estado=None,
            cambiosEstado=[]
        )
        return sismograf_dom
