from ..Estado import Estado


class PendienteDeRevision(Estado):
    """Estado PendienteDeRevision: evento pendiente de revisión manual."""

    def __init__(self, ambito=None):
        super().__init__("Pendiente de Revisión", ambito)

    def getNombreEstado(self):
        return "Pendiente de Revisión"

    def esPendienteDeRevision(self):
        return True

    def bloquear(self, evento, fechaHoraActual, usuario):
        """Transición desde PendienteDeRevision -> BloqueadoEnRevision."""
        from .BloqueadoEnRevision import BloqueadoEnRevision

        nuevo_estado = BloqueadoEnRevision(self.getAmbito())

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

    def anular(self, evento, fechaHoraActual, usuario):
        """Transición desde PendienteDeRevision -> SinRevision (anular)."""
        from .SinRevision import SinRevision

        nuevo_estado = SinRevision(self.getAmbito())

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
