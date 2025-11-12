from .Rol import Rol

class Empleado:
	def __init__(self, nombre: str, apellido: str, mail: str, telefono: str = None, rol: Rol = None):
		self.__nombre = nombre
		self.__apellido = apellido
		self.__mail = mail
		self.__telefono = telefono
		self.__rol = rol

	# Nombre
	def getNombre(self):
		return self.__nombre

	def setNombre(self, nombre: str):
		self.__nombre = nombre

	# Apellido
	def getApellido(self):
		return self.__apellido

	def setApellido(self, apellido: str):
		self.__apellido = apellido

	# Mail
	def getMail(self):
		return self.__mail

	def setMail(self, mail: str):
		self.__mail = mail

	# Telefono
	def getTelefono(self):
		return self.__telefono

	def setTelefono(self, telefono: str):
		self.__telefono = telefono

	# Rol
	def getRol(self):
		return self.__rol

	def setRol(self, rol: Rol):
		self.__rol = rol

def esAdministradorSismos(self):
		"""
		Devuelve True si el empleado tiene asignado un rol cuyo nombre es
		'Administrador de Sismos'. Maneja casos donde rol sea None.
		"""
		if self.__rol is None:
			return False
		return self.__rol.esAdministradorSismos()
