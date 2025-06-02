import datetime
from .Estado import Estado

class CambioEstado:
    def __init__(self, fechaHoraInicio: datetime.datetime, estado: Estado, usuario=None, fechaHoraFin: datetime.datetime = None):
        self.__fechaHoraInicio = fechaHoraInicio  # Antes: fechaHoraDesde
        self.__fechaHoraFin = fechaHoraFin        # Antes: fechaHoraHasta
        self.__estado = estado
        self.__usuario = usuario  # Si quieres guardar el usuario que hizo el cambio

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

    # Usuario (opcional)
    def getUsuario(self):
        return self.__usuario

    def setUsuario(self, usuario):
        self.__usuario = usuario

    # Saber si es el cambio de estado actual
    def esEstadoActual(self):
        return self.__fechaHoraFin is None


