from Modelos.DetalleMuestraSismica import DetalleMuestraSismica

class MuestraSismica:
    def __init__(self, fechaHoraMuestra, detalleMuestraSismica:DetalleMuestraSismica):
        self.__fechaHoraMuestra = fechaHoraMuestra
        self.__detalleMuestraSismica = detalleMuestraSismica

#Fecha y hora de la muestra
    def getFechaHoraMuestra(self):
        return self.__fechaHoraMuestra

    def setFechaHoraMuestra(self, fechaHora):
        self.__fechaHoraMuestra = fechaHora

# Detalle de la muestra sísmica
    def getDetalleMuestraSismica(self):
        return self.__detalleMuestraSismica
    def setDetalleMuestraSismica(self, detalleMuestraSismica):
        self.__detalleMuestraSismica = detalleMuestraSismica

    def getDatos(self):
        detalles = []
        for d in self.getDetalleMuestraSismica():
            detalles.append(d.getDatos())  # <--- Cambia esto
        return {
            'fechaHoraMuestra': str(self.getFechaHoraMuestra()) if self.getFechaHoraMuestra() else 'No disponible',
            'detalle': detalles
        }