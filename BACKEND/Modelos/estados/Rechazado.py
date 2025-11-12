from ..Estado import Estado


class Rechazado(Estado):
    """Estado Rechazado: evento rechazado por el analista."""

    def __init__(self, ambito=None):
        super().__init__("Rechazado", ambito)

    def getNombreEstado(self):
        return "Rechazado"

