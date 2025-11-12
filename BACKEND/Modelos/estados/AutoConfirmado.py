from ..Estado import Estado


class AutoConfirmado(Estado):
    """Estado AutoConfirmado: eventos confirmados automáticamente por el sistema."""

    def __init__(self, ambito=None):
        super().__init__("AutoConfirmado", ambito)

    def getNombreEstado(self):
        return "AutoConfirmado"
