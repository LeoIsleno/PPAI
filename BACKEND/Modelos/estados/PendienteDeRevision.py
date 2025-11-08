from ..Estado import Estado


class PendienteDeRevision(Estado):
    """Estado PendienteDeRevision: evento pendiente de revisión manual."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Pendiente de Revisión"

    def esPendienteDeRevision(self):
        return True

    def bloquear(self, evento, fechaHoraActual, usuario):
        """Transición desde PendienteDeRevision -> BloqueadoEnRevision."""
        from .BloqueadoEnRevision import BloqueadoEnRevision
        
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

        # crear el nuevo cambio
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            pass

        return nuevo_cambio

    def anular(self, evento, fechaHoraActual, usuario):
        """Transición desde PendienteDeRevision -> SinRevision (anular)."""
        from .SinRevision import SinRevision
        
        nuevo_estado = SinRevision(self.getAmbito())
        
        # cerrar cambio actual si existe
        cambio_actual = evento.obtnerEstadoActual()
        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevo_estado)
        except Exception:
            evento.setEstado(nuevo_estado)

        # crear el nuevo cambio
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            pass

        return nuevo_cambio
