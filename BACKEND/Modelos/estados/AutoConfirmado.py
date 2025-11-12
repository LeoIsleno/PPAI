from ..Estado import Estado


class AutoConfirmado(Estado):
    """Estado AutoConfirmado: eventos confirmados automáticamente por el sistema."""

    def __init__(self, ambito=None):
        super().__init__("AutoConfirmado", ambito)

    def getNombreEstado(self):
        return "AutoConfirmado"
<<<<<<< Updated upstream

    def esAutoConfirmado(self):
        """Indica que este estado es 'AutoConfirmado'."""
        return True


    def derivar(self, evento, fechaHoraActual, usuario):
        """Transición AutoConfirmado -> Derivado usando la fábrica de estados.

        Evita referencias directas a la clase `Derivado` (y por tanto errores de
        import). Cierra el cambio actual, crea el nuevo estado mediante
        Estado.from_name y registra el nuevo CambioEstado en el evento.
        """
        # Crear el nuevo estado a través de la fábrica para evitar imports directos
        nuevo_estado = Estado.from_name("Derivado", self.getAmbito())

        # cerrar cambio actual si existe
        cambio_actual = evento.obtenerCambioEstadoActual()
        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)
=======


    """ def derivar(self, evento, fechaHoraActual, usuario, cambiosEstado=None):
        
        # Crear el nuevo estado a través de la fábrica para evitar imports directos
        nuevo_estado = Estado.from_name("Derivado", self.getAmbito())

        # cerrar cambio actual si existe (buscar en la lista de cambios)
        try:
            cambios = cambiosEstado or []
            cambio_actual = next((c for c in cambios if c.getFechaHoraFin() is None), None)
            if cambio_actual:
                try:
                    cambio_actual.setFechaHoraFin(fechaHoraActual)
                except (AttributeError, TypeError):
                    pass
        except Exception:
            cambio_actual = None
>>>>>>> Stashed changes

        # actualizar estado en el contexto
        evento.setEstadoActual(nuevo_estado)

<<<<<<< Updated upstream
        # crear el nuevo cambio y registrar como cambio actual
        nuevo_cambio = evento.crearCambioEstado(nuevo_estado, fechaHoraActual, usuario)
        evento.setCambioEstadoActual(nuevo_cambio)
=======
        from ..CambioEstado import CambioEstado
        nuevo_cambio = CambioEstado(fechaHoraActual, nuevo_estado, usuario)
        try:
            if cambiosEstado is not None:
                cambiosEstado.append(nuevo_cambio)
            else:
                try:
                    evento._cambiosEstado.append(nuevo_cambio)
                except Exception:
                    pass
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
>>>>>>> Stashed changes

        return nuevo_cambio
"""