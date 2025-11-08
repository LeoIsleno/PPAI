from ..Estado import Estado


class Derivado(Estado):
    """Estado Derivado: evento derivado a otra instancia o analista."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Derivado"

    def esDerivado(self):
        return True

    def confirmar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        """Transición desde Derivado -> ConfirmadoPorPersonal."""
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

    def rechazar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        """Transición desde Derivado -> Rechazado."""
        from .Rechazado import Rechazado
        
        if ult_cambio:
            try:
                ult_cambio.setFechaHoraFin(fechaHoraActual)
            except Exception:
                pass

        nuevo_estado = Rechazado(self.getAmbito())
        
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
