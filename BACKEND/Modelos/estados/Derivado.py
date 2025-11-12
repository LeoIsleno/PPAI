from ..Estado import Estado


class Derivado(Estado):

    def __init__(self, ambito=None):
        super().__init__("Derivado", ambito)

    def getNombreEstado(self):
        return "Derivado"