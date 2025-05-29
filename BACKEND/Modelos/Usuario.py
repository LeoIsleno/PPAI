class Usuario:
    def __init__(self, nombre, contraseña, fechaAlta):
        self.__nombre = nombre
        self.__contraseña = contraseña
        self.__fechaAlta = fechaAlta

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

    # Devuelve el usuario logueado (en este contexto, el propio objeto)
    def getUsuarioLogueado(self):
        return self