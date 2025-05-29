from .muestra_sismica import MuestraSismica

class SerieTemporal:
    def __init__(self, fechaHoraInicioRegistroMuestras, fechaHoraRegistro, frecuenciaMuestreo, condicionAlarma, muestraSismica: MuestraSismica):
        self._fechaHoraInicioRegistroMuestras = fechaHoraInicioRegistroMuestras
        self._fechaHoraRegistro = fechaHoraRegistro
        self._frecuenciaMuestreo = frecuenciaMuestreo
        self._condicionAlarma = condicionAlarma
        self._muestraSismica = []
        if muestraSismica is not None:
            self._muestraSismica.append(muestraSismica)

    # Fecha Hora Inicio Registro Muestras
    def getFechaHoraInicioRegistroMuestras(self):
        return self._fechaHoraInicioRegistroMuestras

    def setFechaHoraInicioRegistroMuestras(self, value):
        self._fechaHoraInicioRegistroMuestras = value

    # Fecha Hora Registro
    def getFechaHoraRegistro(self):
        return self._fechaHoraRegistro

    def setFechaHoraRegistro(self, value):
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

    def getDatos(self):
        return {
            'fechaHoraInicioRegistroMuestras': str(self.getFechaHoraInicioRegistroMuestras()) if self.getFechaHoraInicioRegistroMuestras() else 'No disponible',
            'fechaHoraRegistro': str(self.getFechaHoraRegistro()) if self.getFechaHoraRegistro() else 'No disponible',
            'frecuenciaMuestreo': self.getFrecuenciaMuestreo() if self.getFrecuenciaMuestreo() is not None else 'No disponible',
            'condicionAlarma': self.getCondicionAlarma() if self.getCondicionAlarma() is not None else 'No disponible',
            'muestras': [muestra.getDatos() for muestra in self.getMuestraSismica()]
        }
