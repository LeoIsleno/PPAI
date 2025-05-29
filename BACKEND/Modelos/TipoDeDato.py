class TipoDeDato:
    def __init__(self, denominacion, nombreUnidadMedida, valorUmbral):
        self.__denominacion = denominacion
        self.__nombreUnidadMedida = nombreUnidadMedida
        self.__valorUmbral = valorUmbral

# Denominacion
    def getDenominacion(self):
        return self.__denominacion

    def setDenominacion(self, denominacion):
        self.__denominacion = denominacion

# Nombre unidad de medida
    def getNombreUnidadMedida(self):
        return self.__nombreUnidadMedida

    def setNombreUnidadMedida(self, nombreUnidadMedida):
        self.__nombreUnidadMedida = nombreUnidadMedida

# Valor umbral
    def getValorUmbral(self):
        return self.__valorUmbral

    def setValorUmbral(self, valorUmbral):
        self.__valorUmbral = valorUmbral
