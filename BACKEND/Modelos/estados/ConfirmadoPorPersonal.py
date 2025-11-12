from ..Estado import Estado


class ConfirmadoPorPersonal(Estado):
    """Estado ConfirmadoPorPersonal: evento confirmado manualmente por personal."""

    def __init__(self, ambito=None):
        super().__init__("Confirmado por Personal", ambito)
        
    def getNombreEstado(self):
        return "Confirmado por Personal"

    def esConfirmadoPorPersonal(self):
        return True
