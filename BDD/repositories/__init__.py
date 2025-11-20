"""Paquete de repositorios para persistencia.

Cada repositorio encapsula las operaciones de búsqueda/creación/actualización
para una entidad ORM y contiene helpers para convertir desde/ hacia modelos
de dominio cuando corresponda.
"""

from .rol_repository import RolRepository
from .empleado_repository import EmpleadoRepository
from .usuario_repository import UsuarioRepository
from .estado_repository import EstadoRepository
from .origen_repository import OrigenRepository
from .alcance_repository import AlcanceRepository
from .clasificacion_repository import ClasificacionRepository
from .evento_repository import EventoRepository
from .cambio_estado_repository import CambioEstadoRepository
from .serie_repository import SerieRepository
from .IBase_repository import IBaseRepository

__all__ = [
    "RolRepository",
    "EmpleadoRepository",
    "UsuarioRepository",
    "EstadoRepository",
    "OrigenRepository",
    "AlcanceRepository",
    "ClasificacionRepository",
    "EventoRepository",
    "CambioEstadoRepository",
    "SerieRepository",
    "IBaseRepository",
]
