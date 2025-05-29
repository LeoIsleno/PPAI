class ClasificacionSismo:
    def __init__(self, nombre, kmProfundidadDesde, kmProfundidadHasta):
        self.__nombre = nombre
        self.__kmProfundidadDesde = kmProfundidadDesde
        self.__kmProfundidadHasta = kmProfundidadHasta



# Nombre
    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

# Profundidad desde

    def getKmProfundidadDesde(self):
        return self.__kmProfundidadDesde

    def setKmProfundidadDesde(self, kmProfundidadDesde):
        self.__kmProfundidadDesde = kmProfundidadDesde

# Profundidad hasta

    def getKmProfundidadHasta(self):
        return self.__kmProfundidadHasta

    def setKmProfundidadHasta(self, kmProfundidadHasta):
        self.__kmProfundidadHasta = kmProfundidadHasta
