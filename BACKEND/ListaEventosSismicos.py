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


class ListarEventosSismicos:
    """Proveedor de datos persistidos para eventos sísmicos.

    Este módulo centraliza la lectura desde los repositorios/ORM y la
    conversión a objetos de dominio usados por la aplicación.
    """

    @staticmethod
    def crear_eventos_sismicos() -> List[EventoSismico]:
        """Obtener y mapear todos los eventos sísmicos persistidos.

        Returns:
            Lista de instancias de `EventoSismico` del dominio.
        """
        eventos_dom: List[EventoSismico] = []
        with SessionLocal() as db:
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
                resultados.append(AlcanceDom(a.descripcion, a.nombre))
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
                resultados.append(OrigenDom(o.nombre, o.descripcion))
        return resultados

    @staticmethod
    def obtener_estados() -> List[EstadoDom]:
        """Leer y mapear todos los estados desde la base de datos.

        Uses Estado.from_name para crear la instancia concreta del estado.
        """
        resultados: List[EstadoDom] = []
        with SessionLocal() as db:
            orms = EstadoRepository.list_all(db) or []
            for e in orms:
                # Usar fábrica from_name para crear instancia concreta
                estado = EstadoDom.from_name(e.nombre_estado, e.ambito)
                resultados.append(estado)
        return resultados


if __name__ == "__main__":
    evs = ListarEventosSismicos.crear_eventos_sismicos()
    alc = ListarEventosSismicos.obtener_alcances()
    org = ListarEventosSismicos.obtener_origenes()
    est = ListarEventosSismicos.obtener_estados()
    print(f"Eventos: {len(evs)}, Alcances: {len(alc)}, Origenes: {len(org)}, Estados: {len(est)}")