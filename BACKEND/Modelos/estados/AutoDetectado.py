from ..Estado import Estado


class AutoDetectado(Estado):
    """Estado AutoDetectado: eventos sísmicos detectados automáticamente por el sistema."""

    def __init__(self, ambito=None):
        # Usar una forma canonical sin guión para homogeneizar con otras partes
        super().__init__("AutoDetectado", ambito)

    def getNombreEstado(self):
        return "Auto-detectado"

    def esAutoDetectado(self):
        """Indica que este estado es 'AutoDetectado' (predicado usado por el dominio)."""
        return True

    def bloquear(self, evento, fechaHoraActual, usuario):
        """Transición desde AutoDetectado -> BloqueadoEnRevision.

        Cierra el cambio de estado actual (si existe), cambia el estado del
        evento y crea el nuevo CambioEstado delegando al contexto.
        """
        from .BloqueadoEnRevision import BloqueadoEnRevision

        # construir la instancia del siguiente estado
        nuevo_estado = BloqueadoEnRevision(self.getAmbito())

        # cerrar cambio actual si existe
        cambio_actual = evento.obtenerCambioEstadoActual()
        if cambio_actual:
            # Llamar directamente; si el dominio está mal formado se propagará la excepción
            # (se evita el uso de try/except solicitada por el cambio).
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        # actualizar estado en el contexto
        # Llamada directa al método principal; si el objeto no implementa el método
        # la excepción deberá propagarse para que sea visible en capas superiores.
        evento.setEstadoActual(nuevo_estado)

        # crear el nuevo cambio y notificar al evento cuál es el cambio actual
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        # Registrar el cambio actual
        evento.setCambioEstadoActual(nuevo_cambio)

