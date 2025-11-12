from ..Estado import Estado


class ConfirmadoPorPersonal(Estado):
    """Estado ConfirmadoPorPersonal: evento confirmado manualmente por personal."""

    def __init__(self, ambito=None):
        super().__init__("Confirmado por Personal", ambito)

    def esConfirmadoPorPersonal(self):
        return True

    def cerrar(self, evento, fechaHoraActual, usuario):
        """Transición desde ConfirmadoPorPersonal -> Cerrado."""
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
