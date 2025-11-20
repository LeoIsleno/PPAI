from typing import List, Optional, Any

from BDD.database import SessionLocal
from BDD.repositories.evento_repository import EventoRepository
from BDD.repositories.alcance_repository import AlcanceRepository
from BDD.repositories.origen_repository import OrigenRepository
from BDD.repositories.estado_repository import EstadoRepository

# Importar modelos de dominio usando rutas absolutas del paquete para evitar
# problemas al ejecutar desde distintos directorios de trabajo.
from BACKEND.Modelos.EventoSismico import EventoSismico
from BACKEND.Modelos.AlcanceSismo import AlcanceSismo as AlcanceDom
from BACKEND.Modelos.OrigenDeGeneracion import OrigenDeGeneracion as OrigenDom
from BACKEND.Modelos.Estado import Estado as EstadoDom
from sqlalchemy.orm import Session


class ListarEventosSismicos:
    """Proveedor de datos persistidos para eventos sísmicos.

    Este módulo centraliza la lectura desde los repositorios/ORM y la
    conversión a objetos de dominio usados por la aplicación.
    """

    @staticmethod
    def crear_eventos_sismicos(db: Session, 
                               sismografos_persistentes: Optional[List[Any]] = None,
                               usuario_global: Optional[Any] = None) -> List[EventoSismico]:
        """Obtener y mapear todos los eventos sísmicos persistidos, usando una sesión externa."""
        eventos_dom: List[EventoSismico] = []
        
        # CORRECCIÓN: Usar la sesión 'db' que se pasó como parámetro
        orm_events = EventoRepository.list_all(db) or []
        for orm_ev in orm_events:
            ev_dom = EventoRepository.to_domain(orm_ev)
            eventos_dom.append(ev_dom)
            
        return eventos_dom

    @staticmethod
    def obtener_alcances() -> List[AlcanceDom]:
        """Leer y mapear todos los alcances desde la base de datos.

        Returns:
            Lista de `AlcanceSismo` del dominio.
        """
        resultados: List[AlcanceDom] = []
        with SessionLocal() as db:
            orms = AlcanceRepository.list_all(db) or []
            for a in orms:
                resultados.append(AlcanceRepository.to_domain(a)) # <-- USANDO to_domain
        return resultados

    @staticmethod
    def obtener_origenes() -> List[OrigenDom]:
        """Leer y mapear todos los orígenes desde la base de datos.

        Returns:
            Lista de `OrigenDeGeneracion` del dominio.
        """
        resultados: List[OrigenDom] = []
        with SessionLocal() as db:
            orms = OrigenRepository.list_all(db) or []
            for o in orms:
                resultados.append(OrigenRepository.to_domain(o)) # <-- USANDO to_domain
        return resultados

    @staticmethod
    def obtener_estados() -> List[EstadoDom]:
        """Leer y mapear todos los estados desde la base de datos."""
        resultados: List[EstadoDom] = []
        with SessionLocal() as db:
            orms = EstadoRepository.list_all(db) or []
            for e in orms:
                # CORRECCIÓN: Delegar al repositorio para la conversión
                estado = EstadoRepository.to_domain(e)
                resultados.append(estado)
        return resultados


if __name__ == "__main__":
    evs = ListarEventosSismicos.crear_eventos_sismicos()
    alc = ListarEventosSismicos.obtener_alcances()
    org = ListarEventosSismicos.obtener_origenes()
    est = ListarEventosSismicos.obtener_estados()
    print(f"Eventos: {len(evs)}, Alcances: {len(alc)}, Origenes: {len(org)}, Estados: {len(est)}")