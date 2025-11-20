from typing import List, Any
from sqlalchemy.orm import Session # Se usa para el tipado del parámetro 'db'
from abc import ABC, abstractmethod

class IBaseRepository(ABC):
    """
    Interfaz que define el contrato de métodos para todos los repositorios 
    concretos (Evento, Usuario, etc.) en la capa BDD.
    """
    
    @abstractmethod
    def get_by_id(db: Session, id: int) -> Any:
        """Contrato: Recupera una entidad por su ID."""
        # Se deja vacío; la implementación va en las clases concretas.
        raise NotImplementedError("El método get_by_id debe ser implementado por el repositorio concreto.")

    @abstractmethod
    def list_all(db: Session) -> List[Any]:
        """Contrato: Lista todas las entidades de este tipo."""
        raise NotImplementedError("El método list_all debe ser implementado por el repositorio concreto.")
        
    @abstractmethod
    def from_domain(db: Session, objeto_dominio: Any) -> Any:
        """Contrato: Convierte y persiste un objeto de dominio a un objeto ORM."""
        raise NotImplementedError("El método from_domain debe ser implementado por el repositorio concreto.")
        
    @abstractmethod
    def to_domain(orm_objeto: Any) -> Any:
        """Contrato: Mapea un objeto ORM a un objeto de dominio."""
        raise NotImplementedError("El método to_domain debe ser implementado por el repositorio concreto.")
        
    @abstractmethod
    def delete(db: Session, orm_objeto: Any):
        """Contrato: Elimina un objeto ORM."""
        raise NotImplementedError("El método delete debe ser implementado por el repositorio concreto.")