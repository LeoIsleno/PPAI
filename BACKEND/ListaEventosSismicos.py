import os
import sys
import logging
from pathlib import Path
from typing import List

# Configurar logging simple
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Asegurar que la raíz del proyecto esté en sys.path para poder importar paquetes locales
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from BDD.database import SessionLocal
from BDD.repositories.evento_repository import EventoRepository
from BDD.repositories.alcance_repository import AlcanceRepository
from BDD.repositories.origen_repository import OrigenRepository
from BDD.repositories.estado_repository import EstadoRepository

# Clases de dominio (Modelos) - intentar importación relativa primero, luego absoluta
try:
    from .Modelos.EventoSismico import EventoSismico
    from .Modelos.AlcanceSismo import AlcanceSismo as AlcanceDom
    from .Modelos.OrigenDeGeneracion import OrigenDeGeneracion as OrigenDom
    from .Modelos.Estado import Estado as EstadoDom
except ImportError:
    # Si falla la importación relativa, usar importación absoluta
    from BACKEND.Modelos.EventoSismico import EventoSismico
    from BACKEND.Modelos.AlcanceSismo import AlcanceSismo as AlcanceDom
    from BACKEND.Modelos.OrigenDeGeneracion import OrigenDeGeneracion as OrigenDom
    from BACKEND.Modelos.Estado import Estado as EstadoDom


class ListarEventosSismicos:
    """Proveedor de datos persistidos para eventos sísmicos."""

    @staticmethod
    def crear_eventos_sismicos(sismografos_persistentes=None, usuario_global=None) -> List[EventoSismico]:
        eventos_dom = []
        db = SessionLocal()
        try:
            orm_events = EventoRepository.list_all(db) or []
            for orm_ev in orm_events:
                try:
                    ev_dom = EventoRepository.to_domain(orm_ev)
                    eventos_dom.append(ev_dom)
                except Exception:
                    logger.debug("Omitiendo evento corrupto durante la transformación", exc_info=True)
                    continue
        except Exception:
            logger.exception("Error al obtener eventos desde la base de datos.")
            raise
        finally:
            db.close()
        return eventos_dom

    @staticmethod
    def obtener_alcances() -> List[AlcanceDom]:
        resultados: List[AlcanceDom] = []
        db = SessionLocal()
        try:
            orms = AlcanceRepository.list_all(db) or []
            for a in orms:
                try:
                    resultados.append(AlcanceDom(a.descripcion, a.nombre))
                except Exception:
                    resultados.append(AlcanceDom(getattr(a, "descripcion", None), getattr(a, "nombre", None)))
        except Exception:
            logger.exception("Error al obtener alcances desde la base de datos.")
            raise
        finally:
            db.close()
        return resultados

    @staticmethod
    def obtener_origenes() -> List[OrigenDom]:
        resultados: List[OrigenDom] = []
        db = SessionLocal()
        try:
            orms = OrigenRepository.list_all(db) or []
            for o in orms:
                try:
                    resultados.append(OrigenDom(o.nombre, o.descripcion))
                except Exception:
                    resultados.append(OrigenDom(getattr(o, "nombre", None), getattr(o, "descripcion", None)))
        except Exception:
            logger.exception("Error al obtener orígenes desde la base de datos.")
            raise
        finally:
            db.close()
        return resultados

    @staticmethod
    def obtener_estados() -> List[EstadoDom]:
        resultados: List[EstadoDom] = []
        db = SessionLocal()
        try:
            orms = EstadoRepository.list_all(db) or []
            for e in orms:
                try:
                    # Usar fábrica from_name para crear instancia concreta
                    estado = EstadoDom.from_name(e.nombre_estado, e.ambito)
                    resultados.append(estado)
                except Exception:
                    # Fallback con getattr
                    nombre = getattr(e, "nombre_estado", None)
                    ambito = getattr(e, "ambito", None)
                    estado = EstadoDom.from_name(nombre, ambito)
                    resultados.append(estado)
        except Exception:
            logger.exception("Error al obtener estados desde la base de datos.")
            raise
        finally:
            db.close()
        return resultados


if __name__ == "__main__":
    evs = ListarEventosSismicos.crear_eventos_sismicos()
    alc = ListarEventosSismicos.obtener_alcances()
    org = ListarEventosSismicos.obtener_origenes()
    est = ListarEventosSismicos.obtener_estados()
    print(f"Eventos: {len(evs)}, Alcances: {len(alc)}, Origenes: {len(org)}, Estados: {len(est)}")