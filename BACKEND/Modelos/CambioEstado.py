import datetime
from .Estado import Estado
from .Usuario import Usuario


class CambioEstado:
    def __init__(self, fechaHoraInicio: datetime.datetime, estado: Estado, usuario: Usuario, fechaHoraFin: datetime.datetime = None):
        self.__fechaHoraInicio = fechaHoraInicio  
        self.__fechaHoraFin = fechaHoraFin        
        self.__estado = estado
        self.__usuario = usuario  

    # FechaHoraInicio
    def getFechaHoraInicio(self):
        return self.__fechaHoraInicio

    def setFechaHoraInicio(self, fechaHoraInicio):
        self.__fechaHoraInicio = fechaHoraInicio

    # FechaHoraFin
    def getFechaHoraFin(self):
        return self.__fechaHoraFin

    def setFechaHoraFin(self, fechaHoraFin):
        self.__fechaHoraFin = fechaHoraFin

    # Estado
    def getEstado(self):
        return self.__estado

    def setEstado(self, estado):
        self.__estado = estado

    # Usuario
    def getUsuario(self):
        return self.__usuario

    def setUsuario(self, usuario: Usuario):
        self.__usuario = usuario

    # Saber si es el cambio de estado actual
    def esEstadoActual(self):
        return self.__fechaHoraFin is None


