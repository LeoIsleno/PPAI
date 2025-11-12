from abc import ABC


class Estado(ABC):
    """Clase base para todos los estados.

    Contiene el nombre del estado y el ámbito (p.ej. 'EventoSismico').
    Las subclases concretas pueden sobreescribir los métodos de transición
    si corresponden.
    """

    def __init__(self, nombre: str = None, ambito: str = None):
        self._nombre = nombre
        self._ambito = ambito

    def getAmbito(self):
        return self._ambito

    def setAmbito(self, ambito):
        self._ambito = ambito

    def getNombreEstado(self):
        return self._nombre

    # Operaciones que pueden implicar una transición de estado.
    # Las subclases pueden cerrar el cambio de estado actual consultando
    # directamente `evento.obtenerCambioEstadoActual()` cuando sea necesario.
    def bloquear(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()

    def rechazar(self, evento, fechaHoraActual, usuario):
        # Comportamiento por defecto: no hacer nada y devolver None.
        return None

    def confirmar(self, evento, fechaHoraActual, usuario):
        return None

    def derivar(self, evento, fechaHoraActual, usuario):
        return None

    def cerrar(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()

    def anular(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()

    def esAmbitoEventoSismico(self):
        return self.getAmbito() == "EventoSismico"

    @classmethod
    def from_name(cls, nombre: str, ambito=None):
        """Fábrica: crea una instancia del estado concreto a partir de su nombre.

        Este método importa las clases concretas del paquete `estados` y
        construye la instancia usando la convención de que el constructor
        acepta el parámetro `ambito` (el nombre se asigna internamente).
        """
        from .estados import (
            AutoDetectado, AutoConfirmado, PendienteDeCierre, Derivado,
            ConfirmadoPorPersonal, Cerrado, Rechazado, BloqueadoEnRevision,
            PendienteDeRevision, SinRevision
        )

        if nombre is None:
            return AutoDetectado(ambito)

        n = nombre.strip()

        # Mapeo de nombres a clases
        estados_map = {
            "Auto-detectado": AutoDetectado,
            "AutoDetectado": AutoDetectado,
            "Auto-confirmado": AutoConfirmado,
            "AutoConfirmado": AutoConfirmado,
            "PendienteDeCierre": PendienteDeCierre,
            "Pendiente de Cierre": PendienteDeCierre,
            "Derivado": Derivado,
            "ConfirmadoPorPersonal": ConfirmadoPorPersonal,
            "Confirmado por Personal": ConfirmadoPorPersonal,
            "Cerrado": Cerrado,
            "Rechazado": Rechazado,
            "BloqueadoEnRevision": BloqueadoEnRevision,
            "Bloqueado en Revisión": BloqueadoEnRevision,
            "PendienteDeRevision": PendienteDeRevision,
            "Pendiente de Revisión": PendienteDeRevision,
            "SinRevision": SinRevision,
            "Sin Revisión": SinRevision
        }

        estado_clase = estados_map.get(n)
        if estado_clase:
            return estado_clase(ambito)

        # Fallback a AutoDetectado si no se reconoce
        return AutoDetectado(ambito)


def _es_ambito_evento_sismico(ambito):
    """Método auxiliar para identificar el ámbito de evento sismico"""
    return ambito == "EventoSismico"

