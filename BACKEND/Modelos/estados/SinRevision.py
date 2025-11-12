from ..Estado import Estado


class SinRevision(Estado):
    """Estado SinRevision: evento sin revisión, anulado."""

    def __init__(self, ambito=None):
        super().__init__("SinRevision", ambito)

    def getNombreEstado(self):
        return "SinRevision"

