from ListaEventosSismicos import ListarEventosSismicos as listaEventos
from Modelos.Sismografo import Sismografo
from Modelos.EstacionSismologica import EstacionSismologica
from Modelos.MuestraSismica import MuestraSismica
from Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from Modelos.TipoDeDato import TipoDeDato
from Modelos.SerieTemporal import SerieTemporal
from Modelos.CambioEstado import CambioEstado
from Modelos.Estado import Estado
from random import randint, choice
from datetime import datetime, timedelta

# Intent: recuperar sismografos desde la DB cuando estén disponibles
from BDD.database import SessionLocal
from BDD import orm_models

# Supongamos que lista_eventos_sismicos es una lista de eventos sismicos ya creada en listaEventosSismicos.py
class ListaSismografos:
    def __init__(self, empleado=None):
        # Intent: devolver sismografos mapeados desde la DB. Si se desea mantener
        # el antiguo generador en memoria, el caller puede proveer objetos manuales.
        from BDD.repositories.sismografo_repository import SismografoRepository

        try:
            db = SessionLocal()
            orm_sismos = db.query(orm_models.Sismografo).all()
            self.sismografos = [SismografoRepository.to_domain(s) for s in orm_sismos]
        except Exception:
            self.sismografos = []
        finally:
            try:
                db.close()
            except Exception:
                pass

        
    @staticmethod
    def _map_orm_sismografo_to_domain(orm_s):
        """Compatibility helper kept for callers that used it previously.

        Internally repositories provide the canonical `to_domain` mapper, but
        this method mirrors that behavior for compatibility.
        """
        from BDD.repositories.sismografo_repository import SismografoRepository
        return SismografoRepository.to_domain(orm_s)
