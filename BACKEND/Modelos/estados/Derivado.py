from ..Estado import Estado


class Derivado(Estado):
    """Estado Derivado: evento derivado a otra instancia o analista."""

    def __init__(self, ambito=None):
        super().__init__("Derivado", ambito)

    def esDerivado(self):
        return True

    def confirmar(self, evento, fechaHoraActual, usuario):
        """Transición desde Derivado -> ConfirmadoPorPersonal."""
        from .ConfirmadoPorPersonal import ConfirmadoPorPersonal

        cambio_actual = evento.obtenerCambioEstadoActual()
        if cambio_actual:
            try:
                cambio_actual.setFechaHoraFin(fechaHoraActual)
            except (AttributeError, TypeError):
                # Si el cambio no tiene el método esperado o el tipo es incorrecto,
                # dejamos que siga el flujo; no atrapamos excepciones generales aquí.
                pass

        nuevo_estado = ConfirmadoPorPersonal(self.getAmbito())

        try:
            evento.setEstadoActual(nuevo_estado)
        except (AttributeError, TypeError):
            # Fallback a setEstado si la API del evento no implementa setEstadoActual
            evento.setEstado(nuevo_estado)

        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except (AttributeError, TypeError):
            # Ignorar si la API no soporta setCambioEstadoActual
            pass

        return nuevo_cambio

    def rechazar(self, evento, fechaHoraActual, usuario):
        """Transición desde Derivado -> Rechazado."""
        from .Rechazado import Rechazado

        cambio_actual = evento.obtenerCambioEstadoActual()
        if cambio_actual:
            try:
                cambio_actual.setFechaHoraFin(fechaHoraActual)
            except (AttributeError, TypeError):
                pass

        nuevo_estado = Rechazado(self.getAmbito())

        try:
            evento.setEstadoActual(nuevo_estado)
        except (AttributeError, TypeError):
            evento.setEstado(nuevo_estado)

        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except (AttributeError, TypeError):
            pass

        return nuevo_cambio
