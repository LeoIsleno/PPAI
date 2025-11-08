from ..Estado import Estado


class BloqueadoEnRevision(Estado):
    """Estado BloqueadoEnRevision: evento bloqueado para revisión manual."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Bloqueado en Revisión"

    def esBloqueadoEnRevision(self):
        return True

    def rechazar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        """Transición BloqueadoEnRevision -> Rechazado.

        Cierra el cambio actual (si se pasa `ult_cambio`), cambia el estado y
        crea el nuevo CambioEstado en el contexto.
        """
        from .Rechazado import Rechazado
        
        # cerrar el cambio que se recibió (si aplica)
        if ult_cambio:
            try:
                ult_cambio.setFechaHoraFin(fechaHoraActual)
            except Exception:
                # ignorar errores leves para compatibilidad
                pass

        nuevo_estado = Rechazado(self.getAmbito())
        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevo_estado)
        except Exception:
            evento.setEstado(nuevo_estado)

        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            pass

        return nuevo_cambio

    def confirmar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        """Transición BloqueadoEnRevision -> ConfirmadoPorPersonal.

        Cierra el cambio actual (si se pasa `ult_cambio`), cambia el estado y
        crea el nuevo CambioEstado en el contexto.
        """
        from .ConfirmadoPorPersonal import ConfirmadoPorPersonal
        
        if ult_cambio:
            try:
                ult_cambio.setFechaHoraFin(fechaHoraActual)
            except Exception:
                pass

        nuevo_estado = ConfirmadoPorPersonal(self.getAmbito())
        try:
            evento.setEstadoActual(nuevo_estado)
        except Exception:
            evento.setEstado(nuevo_estado)

        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            pass

        return nuevo_cambio

    def derivar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        """Transición BloqueadoEnRevision -> Derivado.

        Cierra el cambio actual (si se pasa `ult_cambio`), cambia el estado a
        Derivado y crea el nuevo CambioEstado para solicitar revisión a experto.
        """
        from .Derivado import Derivado
        
        if ult_cambio:
            try:
                ult_cambio.setFechaHoraFin(fechaHoraActual)
            except Exception:
                pass

        nuevo_estado = Derivado(self.getAmbito())
        try:
            evento.setEstadoActual(nuevo_estado)
        except Exception:
            evento.setEstado(nuevo_estado)

        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            pass

        return nuevo_cambio
