from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from .rol_repository import RolRepository
from BACKEND.Modelos.Rol import Rol
from BACKEND.Modelos.Empleado import Empleado
from .IBase_repository import IBaseRepository


class EmpleadoRepository(IBaseRepository):
    @staticmethod
    def from_domain(db: Session, empleado):
        mail = empleado.getMail()
        existente = db.query(orm_models.Empleado).filter_by(mail=mail).first() if mail else None
        
        if existente:
            existente.nombre = empleado.getNombre()
            existente.apellido = empleado.getApellido()
            existente.telefono = empleado.getTelefono()
        else:
            existente = orm_models.Empleado(
                nombre=empleado.getNombre(),
                apellido=empleado.getApellido(),
                mail=mail,
                telefono=empleado.getTelefono()
            )
            db.add(existente)

        rol = empleado.getRol()
        if rol:
            existente.rol = RolRepository.get_or_create(db, rol)

        return existente

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Empleado]:
        return db.query(orm_models.Empleado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Empleado).all()

    @staticmethod
    def delete(db: Session, empleado: orm_models.Empleado):
        db.delete(empleado)

    @staticmethod
    def to_domain(orm_empleado):
        """Mapea un objeto ORM Empleado a un objeto de dominio Empleado."""
        if not orm_empleado:
            return None
        
        rol = None
        if orm_empleado.rol:
            rol = Rol(
                orm_empleado.rol.nombre,
                orm_empleado.rol.descripcion
            )
            
        return Empleado(
            orm_empleado.nombre,
            orm_empleado.apellido,
            orm_empleado.mail,
            orm_empleado.telefono,
            rol
        )
