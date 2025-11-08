from ..Estado import Estado


class AutoDetectado(Estado):
    """Estado AutoDetectado: eventos sísmicos detectados automáticamente por el sistema."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Auto-detectado"

    def esAutoDetectado(self):
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
        cambio_actual = evento.obtnerEstadoActual()
        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevo_estado)
        except Exception:
            evento.setEstado(nuevo_estado)

        # crear el nuevo cambio y notificar al evento cuál es el cambio actual
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            pass

        return nuevo_cambio
