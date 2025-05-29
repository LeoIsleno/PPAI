from .usuario import Usuario

class Sesion:
    def __init__(self, fechaHoraDesde, fechaHoraHasta, usuario: Usuario):
        self.__fechaHoraDesde = fechaHoraDesde
        self.__fechaHoraHasta = fechaHoraHasta
        self.__usuario = usuario


# FechaHoraDesde
    def getFechaHoraDesde(self):
        return self.__fechaHoraDesde

    def setFechaHoraDesde(self, fechaHoraDesde):
        self.__fechaHoraDesde = fechaHoraDesde

# FechaHoraHasta
    def getFechaHoraHasta(self):
        return self.__fechaHoraHasta

    def setFechaHoraHasta(self, fechaHoraHasta):
        self.__fechaHoraHasta = fechaHoraHasta

# Usuario
    def getUsuario(self):
        return self.__usuario

    def setUsuario(self, usuario):
        self.__usuario = usuario

    def obtenerUsuario(self):
        return self.__usuario