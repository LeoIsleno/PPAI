from ..Estado import Estado


class BloqueadoEnRevision(Estado):
    """Estado BloqueadoEnRevision: evento bloqueado para revisión manual."""

    def __init__(self, ambito=None):
        # Nombre canonical sin espacios ni acentos para consistencia
        super().__init__("BloqueadoEnRevision", ambito)

    def getNombreEstado(self):
        return "BloqueadoEnRevision"

    def obtenerCambioEstadoActual(self, cambiosEstado, fechaHoraActual):
        """Devuelve el cambio de estado actual (el que está abierto) o None.

        La función es robusta: intenta usar `esEstadoActual()` si está disponible
        en el objeto cambio; si no, comprueba `getFechaHoraFin()` o el
        atributo `fechaHoraFin` para determinar si está abierto.
        """
        try:
            cambios = cambiosEstado or []
            cambio_actual = next((c for c in cambios if c.esEstadoActual()), None)
            if cambio_actual:
                try:
                    cambio_actual.setFechaHoraFin(fechaHoraActual)
                except (AttributeError, TypeError):
                    pass
        except Exception:
            cambio_actual = None

    def crearProximoEstado(self, nuevoEstado):
        """Resuelve/crea la instancia del próximo Estado.

        Parámetros:
        - nuevoEstado: puede ser una instancia de Estado o un nombre (str).
        Si `nuevoEstado` es un nombre desconocido para la fábrica, se crea
        dinámicamente una instancia genérica de `Estado` con ese nombre en
        lugar de devolver un fallback a otro tipo.
        """
        # Si ya es una instancia, devolverla tal cual
        if isinstance(nuevoEstado, Estado):
            return nuevoEstado

        # Resolver por nombre mediante la fábrica
        nombreSolicitado = str(nuevoEstado) if nuevoEstado is not None else None
        instancia = Estado.from_name(nombreSolicitado, self.getAmbito())

        # Normalizar nombres para comparar si la fábrica realmente reconoció el nombre
        def _norm(s):
            if not s:
                return ""
            return s.strip().lower().replace(" ", "").replace("-", "")

        if nombreSolicitado is None:
            return instancia

        solicitado_norm = _norm(nombreSolicitado)
        encontrado_norm = _norm(instancia.getNombreEstado() if hasattr(instancia, 'getNombreEstado') else instancia.__class__.__name__)

        if solicitado_norm != encontrado_norm:
            # La fábrica devolvió un fallback distinto; crear un Estado genérico con el nombre solicitado
            return Estado(nombreSolicitado, self.getAmbito())

        return instancia

    def crearCambioEstado(self, nuevoEstado, fechaHoraActual, usuario):
        from ..CambioEstado import CambioEstado
        """
        Crea y devuelve una instancia real de CambioEstado (no un dict).
        """
        # crear la instancia concreta de CambioEstado definida en Modelos/CambioEstado.py
        nuevoCambio = CambioEstado(fechaHoraActual, nuevoEstado, usuario, fechaHoraFin=None)
        return nuevoCambio

    def rechazar(self, evento, fechaHoraActual, usuario, cambiosEstado):
        """Transición desde BloqueadoEnRevision -> Rechazado.

        Cierra el cambio de estado actual (si existe), cambia el estado del
        evento y crea el nuevo CambioEstado delegando al contexto.
        """
        # cerrar cambio actual si existe (buscar en la lista de cambios)
        self.obtenerCambioEstadoActual(cambiosEstado, fechaHoraActual)

        nuevoEstado = self.crearProximoEstado("Rechazado")

        nuevoCambio = self.crearCambioEstado(nuevoEstado, fechaHoraActual, usuario)

        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevoEstado)
        except (AttributeError, TypeError):
            evento.setEstado(nuevoEstado)
        try:
            evento.setCambioEstadoActual(nuevoCambio)
        except Exception:
            try:
                evento._cambioEstadoActual = nuevoCambio
            except Exception:
                pass

    def confirmar(self, evento, fechaHoraActual, usuario, cambiosEstado):
        """Transición desde BloqueadoEnRevision -> ConfirmadoPorPersonal.

        Cierra el cambio de estado actual (si existe), cambia el estado del
        evento y crea el nuevo CambioEstado delegando al contexto.
        """
        # cerrar cambio actual si existe (buscar en la lista de cambios)
        self.obtenerCambioEstadoActual(cambiosEstado, fechaHoraActual)

        nuevoEstado = self.crearProximoEstado("ConfirmadoPorPersonal")

        nuevoCambio = self.crearCambioEstado(nuevoEstado, fechaHoraActual, usuario)

        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevoEstado)
        except (AttributeError, TypeError):
            evento.setEstado(nuevoEstado)
        try:
            evento.setCambioEstadoActual(nuevoCambio)
        except Exception:
            try:
                evento._cambioEstadoActual = nuevoCambio
            except Exception:
                pass

    def derivar(self, evento, fechaHoraActual, usuario, cambiosEstado):
        """Transición desde BloqueadoEnRevision -> Derivado.

        Cierra el cambio de estado actual (si existe), cambia el estado del
        evento y crea el nuevo CambioEstado delegando al contexto.
        """
        # cerrar cambio actual si existe (buscar en la lista de cambios)
        self.obtenerCambioEstadoActual(cambiosEstado, fechaHoraActual)

        nuevoEstado = self.crearProximoEstado("Derivado")

        nuevoCambio = self.crearCambioEstado(nuevoEstado, fechaHoraActual, usuario)

        # actualizar estado en el contexto
        try:
            evento.setEstadoActual(nuevoEstado)
        except (AttributeError, TypeError):
            evento.setEstado(nuevoEstado)
        try:
            evento.setCambioEstadoActual(nuevoCambio)
        except Exception:
            try:
                evento._cambioEstadoActual = nuevoCambio
            except Exception:
                pass
