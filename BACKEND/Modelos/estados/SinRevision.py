from ..Estado import Estado


class SinRevision(Estado):
    """Estado SinRevision: evento sin revisión, anulado."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Sin Revisión"

    def esSinRevision(self):
        return True
