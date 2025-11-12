from ..Estado import Estado


class AutoConfirmado(Estado):
    """Estado AutoConfirmado: eventos confirmados automáticamente por el sistema."""

    def __init__(self, ambito=None):
        super().__init__("Auto-confirmado", ambito)

    def getNombreEstado(self):
        return "Auto-confirmado"

    def esAutoConfirmado(self):
        """Indica que este estado es 'AutoConfirmado'."""
        return True


    def derivar(self, evento, fechaHoraActual, usuario):
        """Transición desde AutoConfirmado -> Derivado."""
        from .Derivado import Derivado

        nuevo_estado = Derivado(self.getAmbito())

        # cerrar cambio actual si existe
        cambio_actual = evento.obtenerCambioEstadoActual()
        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        # actualizar estado en el contexto
        evento.setEstadoActual(nuevo_estado)

        # crear el nuevo cambio
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        evento.setCambioEstadoActual(nuevo_cambio)

        return nuevo_cambio
