from ..Estado import Estado


class PendienteDeRevision(Estado):
    """Estado PendienteDeRevision: evento pendiente de revisión manual."""

    def __init__(self, ambito=None):
        super().__init__("PendienteDeRevision", ambito)

    def getNombreEstado(self):
        return "PendienteDeRevision"
