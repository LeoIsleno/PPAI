from ..Estado import Estado


class AutoDetectado(Estado):
    """Estado AutoDetectado: eventos sísmicos detectados automáticamente por el sistema."""

    def __init__(self, ambito=None):
        # Usar una forma canonical sin guión para homogeneizar con otras partes
        super().__init__("AutoDetectado", ambito)

    def getNombreEstado(self):
        # Devolver el nombre canonical usado por la aplicación
        return "AutoDetectado"

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
    
    def crearProximoEstado(self,  nuevoEstado):
        """Resuelve/crea la instancia del próximo Estado.

        Parámetros:
        - nuevo_estado: puede ser una instancia de Estado o un nombre (str).

        Si `nuevo_estado` es un nombre desconocido para la fábrica, se crea
        dinámicamente una instancia genérica de `Estado` con ese nombre en
        lugar de devolver un fallback a otro tipo.
        """
        # Si ya es una instancia, devolverla tal cual
        if isinstance(nuevoEstado, Estado):
            return nuevoEstado

        # Resolver por nombre mediante la fábrica
        nombre_solicitado = str(nuevoEstado) if nuevoEstado is not None else None
        instancia = Estado.from_name(nombre_solicitado, self.getAmbito())

        # Normalizar nombres para comparar si la fábrica realmente reconoció el nombre
        def _norm(s):
            if not s:
                return ""
            return s.strip().lower().replace(" ", "").replace("-", "")

        if nombre_solicitado is None:
            return instancia

        solicitado_norm = _norm(nombre_solicitado)
        encontrado_norm = _norm(instancia.getNombreEstado() if hasattr(instancia, 'getNombreEstado') else instancia.__class__.__name__)

        if solicitado_norm != encontrado_norm:
            # La fábrica devolvió un fallback distinto; crear un Estado genérico con el nombre solicitado
            return Estado(nombre_solicitado, self.getAmbito())

        return instancia

    def crearCambioEstado(self, nuevoEstado, fechaHoraActual, usuario):
        from ..CambioEstado import CambioEstado
        """
        Crea y devuelve una instancia real de CambioEstado (no un dict).
        """
        # crear la instancia concreta de CambioEstado definida en Modelos/CambioEstado.py
        nuevoCambio = CambioEstado(fechaHoraActual, nuevoEstado, usuario, fechaHoraFin=None)
        return nuevoCambio

    def bloquear(self, evento, fechaHoraActual, usuario, cambiosEstado):
        """Transición desde AutoDetectado -> BloqueadoEnRevision.

        Cierra el cambio de estado actual (si existe), cambia el estado del
        evento y crea el nuevo CambioEstado delegando al contexto.
        """
        

        # cerrar cambio actual si existe (buscar en la lista de cambios)
        self.obtenerCambioEstadoActual(cambiosEstado, fechaHoraActual)

        nuevoEstado = self.crearProximoEstado("BloqueadoEnRevision")

        nuevoCambio = self.crearCambioEstado(nuevoEstado, fechaHoraActual, usuario)
        """
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
        """
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

