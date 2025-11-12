from ..Estado import Estado


class PendienteDeCierre(Estado):
    """Estado PendienteDeCierre: evento está esperando ser cerrado."""

    def __init__(self, ambito=None):
        super().__init__("PendienteDeCierre", ambito)

    def getNombreEstado(self):
        return "PendienteDeCierre"
    # La transición a 'Cerrado' se omite aquí porque no existen llamadas
    # estáticas a `cerrar` en el repositorio actual; mantener la clase
    # mínima mejora la mantenibilidad.
