class Rol:
    def __init__(self, nombre: str, descripcion: str = None):
        self.__nombre = nombre
        self.__descripcion = descripcion

    # Nombre
    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre: str):
        self.__nombre = nombre

    # Descripcion
    def getDescripcion(self):
        return self.__descripcion

    def setDescripcion(self, descripcion: str):
        self.__descripcion = descripcion

def esAnalistaSismos(self):
        return self.__nombre == 'Administrador de Sismos'