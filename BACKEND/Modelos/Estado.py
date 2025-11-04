from abc import ABC, abstractmethod


class Estado(ABC):
    """Clase abstracta base para todos los estados.

    Todos los estados concretos deben heredar de aquí. Provee las firmas
    de los métodos que aparecen en los diagramas y helpers comunes.
    """
    def __init__(self, ambito=None):
        self._ambito = ambito

    def getAmbito(self):
        return self._ambito

    def setAmbito(self, ambito):
        self._ambito = ambito

    @abstractmethod
    def getNombreEstado(self):
        pass

    # Operaciones que pueden implicar una transición de estado.
    # Los estados concretos las implementarán cuando corresponda.
    def bloquear(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()

    def rechazar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        raise NotImplementedError()

    def confirmar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        raise NotImplementedError()

    def esAutoDetectado(self):
        return False

    def esBloqueadoEnRevision(self):
        return False

    def esRechazado(self):
        return False

    def esAceptado(self):
        return False

    def esAmbitoEventoSismico(self):
        return self.getAmbito() == "EventoSismico"

    @classmethod
    def from_name(cls, nombre: str, ambito=None):
        """Fábrica: crea una instancia del estado concreto a partir de su nombre."""
        return _state_from_name(nombre, ambito)


class AutoDetectado(Estado):
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
        # construir la instancia del siguiente estado
        nuevo_estado = _state_from_name('BloqueadoEnRevision', self.getAmbito())

        # cerrar cambio actual si existe
        cambio_actual = evento.obtnerEstadoActual()
        if cambio_actual:
            cambio_actual.setFechaHoraFin(fechaHoraActual)

        # actualizar estado en el contexto (dinámica rediseñada)
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


class BloqueadoEnRevision(Estado):
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "BloqueadoEnRevision"

    def esBloqueadoEnRevision(self):
        return True

    def rechazar(self, evento, fechaHoraActual, usuario, ult_cambio=None):
        """Transición BloqueadoEnRevision -> Rechazado.

        Cierra el cambio actual (si se pasa `ult_cambio`), cambia el estado y
        crea el nuevo CambioEstado en el contexto.
        """
        # cerrar el cambio que se recibió (si aplica)
        if ult_cambio:
            try:
                ult_cambio.setFechaHoraFin(fechaHoraActual)
            except Exception:
                # ignorar errores leves para compatibilidad
                pass

        nuevo_estado = _state_from_name('Rechazado', self.getAmbito())
        # actualizar estado en el contexto (dinámica rediseñada)
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
        """Transición BloqueadoEnRevision -> Aceptado.

        Cierra el cambio actual (si se pasa `ult_cambio`), cambia el estado y
        crea el nuevo CambioEstado en el contexto.
        """
        if ult_cambio:
            try:
                ult_cambio.setFechaHoraFin(fechaHoraActual)
            except Exception:
                pass

        nuevo_estado = _state_from_name('Aceptado', self.getAmbito())
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


class Rechazado(Estado):
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Rechazado"

    def esRechazado(self):
        return True


class Aceptado(Estado):
    def __init__(self, ambito=None):
        super().__init__(ambito)

    def getNombreEstado(self):
        return "Aceptado"

    def esAceptado(self):
        return True


def _state_from_name(nombre: str, ambito=None) -> Estado:
    """Factory simple: mapea nombre a instancia de EstadoBase.

    Mantiene compatibilidad con los valores almacenados en la base
    (p. ej. 'Auto-detectado'). Si no se reconoce, devuelve un EstadoBase
    genérico con el nombre crudo como atributo (wrapped en AutoDetectado por defecto).
    """
    if nombre is None:
        # fallback a un estado concreto para evitar instanciar la clase abstracta
        return AutoDetectado(ambito)
    n = nombre.strip()
    if n == "Auto-detectado":
        return AutoDetectado(ambito)
    if n == "BloqueadoEnRevision":
        return BloqueadoEnRevision(ambito)
    if n == "Rechazado":
        return Rechazado(ambito)
    if n == "Aceptado":
        return Aceptado(ambito)
    # valor no reconocido -> usar AutoDetectado como fallback
    return AutoDetectado(ambito)

# Método auxiliar para identificar el ámbito de evento sismico
def _es_ambito_evento_sismico(ambito):
    return ambito == "EventoSismico"

