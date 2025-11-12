from ..Estado import Estado


class PendienteDeCierre(Estado):
    """Estado PendienteDeCierre: evento está esperando ser cerrado."""

    def __init__(self, ambito=None):
        super().__init__("PendienteDeCierre", ambito)

    def getNombreEstado(self):
        return "Pendiente de Cierre"

    def esPendienteDeCierre(self):
        return True

