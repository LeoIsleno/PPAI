from .MuestraSismica import MuestraSismica
from .Estado import Estado
from .CambioEstado import CambioEstado

class SerieTemporal:
    def __init__(self, fechaHoraInicioRegistroMuestras, fechaHoraRegistro, frecuenciaMuestreo, condicionAlarma, muestraSismica: MuestraSismica, estado: Estado = None, cambiosEstado=None):
        self._fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
        self._fechaHoraRegistro = fechaHoraRegistro
        self._frecuenciaMuestreo = frecuenciaMuestreo
        self._condicionAlarma = condicionAlarma
        self._muestraSismica = []
        if muestraSismica is not None:
            self._muestraSismica.append(muestraSismica)
        self._estado = estado
        self._cambiosEstado = cambiosEstado if cambiosEstado is not None else []

    # Getters y setters
    def getFechaHoraInicioRegistroMuestras(self):
        return self._fechaHoraInicioRegistroMuestras

    def setFechaHoraInicioRegistroMuestras(self, value):
        self._fechaHoraInicioRegistroMuestras = value

    def getFechaHoraRegistro(self):
        return self._fechaHoraRegistro

    def setFechaHoraRegistro(self, value):
        self._fechaHoraRegistro = value
        self._fechaHoraRegistro = value

    # Frecuencia Muestreo
    def getFrecuenciaMuestreo(self):
        return self._frecuenciaMuestreo

    def setFrecuenciaMuestreo(self, value):
        self._frecuenciaMuestreo = value

    # Condicion Alarma
    def getCondicionAlarma(self):
        return self._condicionAlarma

    def setCondicionAlarma(self, value):
        self._condicionAlarma = value

    # Muestra Sismica
    def getMuestraSismica(self):
        return self._muestraSismica

    def setMuestraSismica(self, value):
        self._muestraSismica = value

    def agregarMuestraSismica(self, muestra: MuestraSismica):
        self._muestraSismica.append(muestra)

    # Estado
    def getEstado(self):
        return self._estado

    def setEstado(self, estado):
        self._estado = estado

    def getCambiosEstado(self):
        return self._cambiosEstado

    def setCambiosEstado(self, cambios):
        self._cambiosEstado = cambios

    def agregarCambioEstado(self, cambio: CambioEstado):
        self._cambiosEstado.append(cambio)

    def getDatos(self, sismografos):
        return {
            'fechaHoraInicioRegistroMuestras': str(self._fechaHoraInicioRegistroMuestras) if self._fechaHoraInicioRegistroMuestras else 'No disponible',
            'fechaHoraRegistro': str(self._fechaHoraRegistro) if self._fechaHoraRegistro else 'No disponible',
            'frecuenciaMuestreo': self._frecuenciaMuestreo if self._frecuenciaMuestreo is not None else 'No disponible',
            'condicionAlarma': self._condicionAlarma if self._condicionAlarma is not None else 'No disponible',
            'muestras': [muestra.getDatos() for muestra in self._muestraSismica],
            'codigoEstacion': [sismografo.sosDeSerieTemporal(self) for sismografo in sismografos]
        }
