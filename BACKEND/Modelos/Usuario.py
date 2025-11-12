from .Empleado import Empleado


class Usuario:
    def __init__(self, nombre, contraseña, fechaAlta, empleado: Empleado = None):
        self.__nombre = nombre
        self.__contraseña = contraseña
        self.__fechaAlta = fechaAlta
        self.__empleado = empleado

    # Nombre
    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

    # Contraseña
    def getContraseña(self):
        return self.__contraseña

    def setContraseña(self, contraseña):
        self.__contraseña = contraseña

    # Fecha de alta
    def getFechaAlta(self):
        return self.__fechaAlta

    def setFechaAlta(self, fechaAlta):
        self.__fechaAlta = fechaAlta

    # Empleado asociado
    def getEmpleado(self):
        return self.__empleado

    def setEmpleado(self, empleado: Empleado):
        self.__empleado = empleado


    def esAnalistaSismos(self):
        """
        Devuelve True si el usuario tiene un empleado asociado y dicho
        empleado tiene rol 'Administrador de Sismos'.
        """
        empleado = self.getEmpleado()
        if empleado is None:
            return False
        return empleado.esAnalistaSismos()