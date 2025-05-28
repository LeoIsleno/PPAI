from Modelos.tipo_de_dato import TipoDeDato

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
        tipo_dato = self.getTipoDeDato()
        denominacion = tipo_dato.getDenominacion() if tipo_dato else 'No disponible'
        return {
            'valor': self.getValor(),
            'tipoDeDato': denominacion
        }

