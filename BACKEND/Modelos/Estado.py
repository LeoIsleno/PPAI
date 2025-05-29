class Estado:
    def __init__(self, nombreEstado):
        self.__nombreEstado = nombreEstado

# Nombre del estado
    def getNombreEstado(self):
        return self.__nombreEstado

    def setNombreEstado(self, nombre):
        self.__nombreEstado = nombre

# Métodos para verificar el estado
    def esAutoDetectado(self ):
        return self.__nombreEstado == "Auto-detectado"  

    def esBloqueadoEnRevision(self):
        return self.__nombreEstado == "BloqueadoEnRevision"

    def esRechazado(self):
        return self.__nombreEstado == "Rechazado"