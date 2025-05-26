class Estado:
    def __init__(self, nombreEstado, ambito):
        self.__nombreEstado = nombreEstado
        self.__ambito = ambito

# Nombre del estado
    def getNombreEstado(self):
        return self.__nombreEstado

    def setNombreEstado(self, nombre):
        self.__nombreEstado = nombre

# Ambito del estado
    def getAmbito(self):
        return self.__ambito

    def setAmbito(self, ambito):
        self.__ambito = ambito

# Métodos para verificar el estado
    def esAutoDetectado(self ,ambito):
        if ambito == "EventoSismico":
            return self.__nombreEstado == "Auto-detectado"  
        return False

    def esAmbitoEventoSismico(self):
        return self.__ambito == "EventoSismico"

    def esBloqueadoEnRevision(self):
        return self.__nombreEstado == "BloqueadoEnRevision"

    def esRechazado(self):
        return self.__nombreEstado == "Rechazado"