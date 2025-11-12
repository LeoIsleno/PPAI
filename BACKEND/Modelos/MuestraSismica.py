from .DetalleMuestraSismica import DetalleMuestraSismica

class MuestraSismica:
    def __init__(self, fechaHoraMuestra, detalleMuestraSismica: DetalleMuestraSismica | list = None):
        self.__fechaHoraMuestra = fechaHoraMuestra
        # Normalizar detalleMuestraSismica a una lista interna para un manejo uniforme
        if detalleMuestraSismica is None:
            self.__detalleMuestraSismica = []
        elif isinstance(detalleMuestraSismica, list):
            self.__detalleMuestraSismica = detalleMuestraSismica
        else:
            self.__detalleMuestraSismica = [detalleMuestraSismica]

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
        for d in self.__detalleMuestraSismica:
            detalles.append(d.getDatos())  # <--- Cambia esto
        return {
            'fechaHoraMuestra': str(self.__fechaHoraMuestra) if self.__fechaHoraMuestra else 'No disponible',
            'detalle': detalles
        }