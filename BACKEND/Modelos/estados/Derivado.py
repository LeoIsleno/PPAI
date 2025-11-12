from ..Estado import Estado


class Derivado(Estado):

    def __init__(self, ambito=None):
        super().__init__("Derivado", ambito)

    def getNombreEstado(self):
        return "Derivado"

<<<<<<< Updated upstream
    def esDerivado(self):
        return True
=======
    def confirmar(self, evento, fechaHoraActual, usuario, cambiosEstado=None):
        """Transición desde Derivado -> ConfirmadoPorPersonal."""
        # Crear el nuevo estado vía fábrica para evitar import directo
        nuevo_estado = Estado.from_name("ConfirmadoPorPersonal", self.getAmbito())

        try:
            evento.setEstadoActual(nuevo_estado)
        except (AttributeError, TypeError):
            # Fallback a setEstado si la API del evento no implementa setEstadoActual
            evento.setEstado(nuevo_estado)

        from ..CambioEstado import CambioEstado
        nuevo_cambio = CambioEstado(fechaHoraActual, nuevo_estado, usuario)
        try:
            if cambiosEstado is not None:
                cambiosEstado.append(nuevo_cambio)
            else:
                evento._cambiosEstado.append(nuevo_cambio)
        except Exception:
            try:
                evento._cambiosEstado.append(nuevo_cambio)
            except Exception:
                pass
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            try:
                evento._cambioEstadoActual = nuevo_cambio
            except Exception:
                pass

        return nuevo_cambio

    def rechazar(self, evento, fechaHoraActual, usuario, cambiosEstado=None):
        """Transición desde Derivado -> Rechazado."""
        # Crear el nuevo estado vía fábrica para evitar import directo
        nuevo_estado = Estado.from_name("Rechazado", self.getAmbito())

        try:
            evento.setEstadoActual(nuevo_estado)
        except (AttributeError, TypeError):
            evento.setEstado(nuevo_estado)

        from ..CambioEstado import CambioEstado
        nuevo_cambio = CambioEstado(fechaHoraActual, nuevo_estado, usuario)
        try:
            if cambiosEstado is not None:
                cambiosEstado.append(nuevo_cambio)
            else:
                evento._cambiosEstado.append(nuevo_cambio)
        except Exception:
            try:
                evento._cambiosEstado.append(nuevo_cambio)
            except Exception:
                pass
        try:
            evento.setCambioEstadoActual(nuevo_cambio)
        except Exception:
            try:
                evento._cambioEstadoActual = nuevo_cambio
            except Exception:
                pass

        return nuevo_cambio
>>>>>>> Stashed changes
