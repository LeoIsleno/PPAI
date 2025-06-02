from .TipoDeDato import TipoDeDato

class DetalleMuestraSismica:
    def __init__(self, valor, tipo_de_dato: TipoDeDato):
        self.__valor = valor
        self.__tipo_de_dato = tipo_de_dato

# Valor
    def getValor(self):
        return self.__valor

    def setValor(self, valor):
        self.__valor = valor

# Tipo de dato
    def getTipoDeDato(self):
        return self.__tipo_de_dato

    def setTipoDeDato(self, tipo_de_dato):
        self.__tipo_de_dato = tipo_de_dato

    def getDatos(self):
        return {
            "tipoDeDato": self.__tipo_de_dato.getDenominacion() if self.__tipo_de_dato else "No disponible",
            "valor": self.__valor if self.__valor is not None else "No disponible"
        }

