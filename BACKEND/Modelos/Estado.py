class Estado:
    def __init__(self, nombreEstado, ambito=None):
        self.__nombreEstado = nombreEstado
        self.__ambito = ambito

# Nombre del estado
    def getNombreEstado(self):
        return self.__nombreEstado

    def setNombreEstado(self, nombre):
        self.__nombreEstado = nombre

# Ambito
    def getAmbito(self):
        return self.__ambito

    def setAmbito(self, ambito):
        self.__ambito = ambito

# Métodos para verificar el estado
    def esAutoDetectado(self):
        return self.__nombreEstado == "Auto-detectado"  

    def esBloqueadoEnRevision(self):
        return self.__nombreEstado == "BloqueadoEnRevision"

    def esRechazado(self):
        return self.__nombreEstado == "Rechazado"

    def esAmbitoEventoSismico(self):
        return self.__ambito == "EventoSismico"

# --- ESTA PARTE VA FUERA DE LA CLASE ---
