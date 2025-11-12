from ..Estado import Estado


class PendienteDeCierre(Estado):
    """Estado PendienteDeCierre: evento está esperando ser cerrado."""

    def __init__(self, ambito=None):
        super().__init__("Pendiente de Cierre", ambito)

    def getNombreEstado(self):
        return "Pendiente de Cierre"

    def esPendienteDeCierre(self):
        return True

    def cerrar(self, evento, fechaHoraActual, usuario):
        """Transición desde PendienteDeCierre -> Cerrado."""
        from .Cerrado import Cerrado

        nuevo_estado = Cerrado(self.getAmbito())

        # cerrar cambio actual si existe
        cambio_actual = evento.obtenerCambioEstadoActual()
        if cambio_actual:
            try:
                cambio_actual.setFechaHoraFin(fechaHoraActual)
            except (AttributeError, TypeError):
                pass

        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevo_estado)
        except (AttributeError, TypeError):
            evento.setEstado(nuevo_estado)

        # crear el nuevo cambio
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except (AttributeError, TypeError):
            pass

        return nuevo_cambio
