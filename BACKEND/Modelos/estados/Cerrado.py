from ..Estado import Estado


class Cerrado(Estado):
    """Estado Cerrado: evento cerrado, estado final."""

    def __init__(self, ambito=None):
        super().__init__("Cerrado", ambito)

    def getNombreEstado(self):
        return "Cerrado"

    def esCerrado(self):
        return True