class MagnitudRichter:
    """Representa una magnitud expresada en la escala de Richter.

    Attributes:
        descripcion (str): Texto descriptivo corto de la magnitud (opcional).
        numero (float): Valor numérico de la magnitud.
    """
    def __init__(self, descripcionMagnitud: str | None, numero: float):
        self.__descripcion = descripcionMagnitud
        self.__numero = float(numero) if numero is not None else None

    def getDescripcionMagnitud(self):
        return self.__descripcion

    def setDescripcionMagnitud(self, descripcion):
        self.__descripcion = descripcion

    def getNumero(self):
        return self.__numero

    def setNumero(self, numero):
        self.__numero = float(numero) if numero is not None else None

