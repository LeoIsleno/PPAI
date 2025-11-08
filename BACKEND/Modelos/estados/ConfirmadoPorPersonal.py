from ..Estado import Estado


class ConfirmadoPorPersonal(Estado):
    """Estado ConfirmadoPorPersonal: evento confirmado manualmente por personal."""
    
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Confirmado por Personal"

    def esConfirmadoPorPersonal(self):
        return True

    def cerrar(self, evento, fechaHoraActual, usuario):
        """Transición desde ConfirmadoPorPersonal -> Cerrado."""
        from .Cerrado import Cerrado
        
        nuevo_estado = Cerrado(self.getAmbito())
        
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
