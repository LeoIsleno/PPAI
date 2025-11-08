from ..Estado import Estado


class Rechazado(Estado):
    """Estado Rechazado: evento rechazado por el analista."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Rechazado"

    def esRechazado(self):
        return True
