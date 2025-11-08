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
    
    def derivar(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()
    
    def cerrar(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()
    
    def anular(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()

    # Métodos de verificación de estado
    def esAutoDetectado(self):
        return False

    def esAutoConfirmado(self):
        return False

    def esPendienteDeCierre(self):
        return False

    def esDerivado(self):
        return False

    def esConfirmadoPorPersonal(self):
        return False

    def esCerrado(self):
        return False

    def esRechazado(self):
        return False

    def esBloqueadoEnRevision(self):
        return False

    def esPendienteDeRevision(self):
        return False

    def esSinRevision(self):
        return False

    def esAmbitoEventoSismico(self):
        return self.getAmbito() == "EventoSismico"

    @classmethod
    def from_name(cls, nombre: str, ambito=None):
        """Fábrica: crea una instancia del estado concreto a partir de su nombre."""
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

