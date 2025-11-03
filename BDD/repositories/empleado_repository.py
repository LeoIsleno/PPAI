from typing import Optional
from sqlalchemy.orm import Session

from BDD import orm_models
from .rol_repository import RolRepository


class EmpleadoRepository:
    @staticmethod
    def from_domain(db: Session, domain_emp) -> orm_models.Empleado:
        """Convierte un Empleado del dominio a Empleado ORM. No hace commit por defecto."""
        mail = domain_emp.getMail()
        empleado = None
        if mail:
            empleado = db.query(orm_models.Empleado).filter(orm_models.Empleado.mail == mail).first()
        if empleado:
            empleado.nombre = domain_emp.getNombre()
            empleado.apellido = domain_emp.getApellido()
            empleado.telefono = domain_emp.getTelefono()
        else:
            empleado = orm_models.Empleado(
                nombre=domain_emp.getNombre(),
                apellido=domain_emp.getApellido(),
                mail=mail,
                telefono=domain_emp.getTelefono(),
            )
            db.add(empleado)
            # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje

        rol_dom = domain_emp.getRol()
        if rol_dom:
            rol_orm = RolRepository.get_or_create(db, rol_dom)
            empleado.rol = rol_orm

        return empleado

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Empleado]:
        return db.query(orm_models.Empleado).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Empleado).all()

    @staticmethod
    def delete(db: Session, empleado: orm_models.Empleado):
        db.delete(empleado)
