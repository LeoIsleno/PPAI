from typing import List, Optional, Any
from random import randint, choice
from datetime import datetime, timedelta

# Usar imports absolutos del paquete para evitar fallos según el cwd
from BACKEND.ListaEventosSismicos import ListarEventosSismicos as listaEventos
from BACKEND.Modelos.Sismografo import Sismografo
from BACKEND.Modelos.EstacionSismologica import EstacionSismologica
from BACKEND.Modelos.MuestraSismica import MuestraSismica
from BACKEND.Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from BACKEND.Modelos.TipoDeDato import TipoDeDato
from BACKEND.Modelos.SerieTemporal import SerieTemporal
from BACKEND.Modelos.CambioEstado import CambioEstado
from BACKEND.Modelos.Estado import Estado

# Intent: recuperar sismografos desde la DB cuando estén disponibles
from BDD.database import SessionLocal
from BDD import orm_models


class ListaSismografos:
    """Proveedor de sismógrafos que obtiene y mapea los registros desde la BD.

    Si la consulta falla, la instancia mantiene `self.sismografos` como lista vacía,
    pero ahora registramos la excepción para facilitar la depuración.
    """

    def __init__(self, empleado: Optional[Any] = None) -> None:
        """Inicializar la lista de sismógrafos desde la base de datos.

        Args:
            empleado: (opcional) contexto/empleado que podría usarse en el
                mapeo (no utilizado actualmente).
        """
        from BDD.repositories.sismografo_repository import SismografoRepository

        try:
            with SessionLocal() as db:
                orm_sismos = db.query(orm_models.Sismografo).all()
                self.sismografos: List[Sismografo] = [SismografoRepository.to_domain(s) for s in orm_sismos]
        except Exception as ex:
            # Error al cargar sismógrafos desde la base de datos; devolver lista vacía
            print("Error al cargar sismógrafos desde la base de datos; devolviendo lista vacía:", ex)
            self.sismografos = []

    @staticmethod
    def _map_orm_sismografo_to_domain(orm_s) -> Sismografo:
        """Helper de compatibilidad que delega en el repositorio.

        Mantiene la API usada por código legado que llamaba a este método.
        """
        from BDD.repositories.sismografo_repository import SismografoRepository
        return SismografoRepository.to_domain(orm_s)
