class OrigenDeGeneracion:
    def __init__(self, nombre, descripcion):
        self.__nombre = nombre
        self.__descripcion = descripcion

# Nombre
    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

# Descripcion
    def getDescripcion(self):
        return self.__descripcion

    def setDescripcion(self, descripcion):
        self.__descripcion = descripcion
