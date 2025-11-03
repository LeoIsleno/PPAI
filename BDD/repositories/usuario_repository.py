from typing import Optional
from sqlalchemy.orm import Session

from BDD import orm_models
from .empleado_repository import EmpleadoRepository
from .rol_repository import RolRepository
from BACKEND.Modelos.Rol import Rol as DomainRol
from BACKEND.Modelos.Empleado import Empleado as DomainEmpleado
from BACKEND.Modelos.Usuario import Usuario as DomainUsuario


class UsuarioRepository:
    @staticmethod
    def from_domain(db: Session, domain_user: DomainUsuario) -> orm_models.Usuario:
        """Convierte Usuario del dominio a Usuario ORM (crea Empleado/Rol si son necesarios)."""
        nombre = domain_user.getNombre()
        usuario = db.query(orm_models.Usuario).filter(orm_models.Usuario.nombre == nombre).first()
        if usuario:
            usuario.contrasena = domain_user.getContraseña()
            usuario.fecha_alta = domain_user.getFechaAlta()
        else:
            usuario = orm_models.Usuario(
                nombre=domain_user.getNombre(),
                contrasena=domain_user.getContraseña(),
                fecha_alta=domain_user.getFechaAlta(),
            )
            db.add(usuario)
            # No hacer flush aquí - dejar que el commit de la unit_of_work lo maneje

        emp_dom = domain_user.getEmpleado()
        if emp_dom:
            emp_orm = EmpleadoRepository.from_domain(db, emp_dom)
            usuario.empleado = emp_orm

        return usuario


    @staticmethod
    def to_domain(orm_user: orm_models.Usuario) -> DomainUsuario:
        """Convierte una instancia ORM Usuario a la clase de dominio Usuario."""
        from BACKEND.Modelos.Empleado import Empleado as DomainEmpleado
        from BACKEND.Modelos.Rol import Rol as DomainRol

        empleado_dom = None
        if orm_user.empleado:
            rol_dom = None
            if orm_user.empleado.rol:
                rol_dom = DomainRol(orm_user.empleado.rol.nombre, orm_user.empleado.rol.descripcion)
            empleado_dom = DomainEmpleado(
                orm_user.empleado.nombre,
                orm_user.empleado.apellido,
                orm_user.empleado.mail,
                orm_user.empleado.telefono,
                rol_dom,
            )

        user_dom = DomainUsuario(orm_user.nombre, orm_user.contrasena, orm_user.fecha_alta, empleado_dom)
        return user_dom

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Usuario]:
        return db.query(orm_models.Usuario).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Usuario).all()

    @staticmethod
    def delete(db: Session, usuario: orm_models.Usuario):
        db.delete(usuario)
