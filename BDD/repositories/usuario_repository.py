from typing import Optional
from sqlalchemy.orm import Session
from BDD import orm_models
from .empleado_repository import EmpleadoRepository
from BACKEND.Modelos.Rol import Rol
from BACKEND.Modelos.Empleado import Empleado
from BACKEND.Modelos.Usuario import Usuario
from .IBase_repository import IBaseRepository


class UsuarioRepository(IBaseRepository):
    @staticmethod
    def from_domain(db: Session, usuario):
        nombre = usuario.getNombre()
        existente = db.query(orm_models.Usuario).filter_by(nombre=nombre).first()
        
        if existente:
            existente.contrasena = usuario.getContraseña()
            existente.fecha_alta = usuario.getFechaAlta()
        else:
            existente = orm_models.Usuario(
                nombre=nombre,
                contrasena=usuario.getContraseña(),
                fecha_alta=usuario.getFechaAlta()
            )
            db.add(existente)

        empleado = usuario.getEmpleado()
        if empleado:
            existente.empleado = EmpleadoRepository.from_domain(db, empleado)

        return existente

    @staticmethod
    def to_domain(orm_user):
        empleado = None
        if orm_user.empleado:
            rol = None
            if orm_user.empleado.rol:
                rol = Rol(
                    orm_user.empleado.rol.nombre,
                    orm_user.empleado.rol.descripcion
                )
            
            empleado = Empleado(
                orm_user.empleado.nombre,
                orm_user.empleado.apellido,
                orm_user.empleado.mail,
                orm_user.empleado.telefono,
                rol
            )

        return Usuario(
            orm_user.nombre,
            orm_user.contrasena,
            orm_user.fecha_alta,
            empleado
        )

    @staticmethod
    def get_by_id(db: Session, id: int) -> Optional[orm_models.Usuario]:
        return db.query(orm_models.Usuario).get(id)

    @staticmethod
    def list_all(db: Session):
        return db.query(orm_models.Usuario).all()

    @staticmethod
    def delete(db: Session, usuario: orm_models.Usuario):
        db.delete(usuario)
