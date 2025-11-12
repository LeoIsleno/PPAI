from abc import ABC


class Estado(ABC):
    """Clase base para todos los estados."""

    def __init__(self, nombre: str = None, ambito: str = None):
        self._nombre = nombre
        self._ambito = ambito

    def getAmbito(self):
        return self._ambito

    def setAmbito(self, ambito):
        self._ambito = ambito

    def getNombreEstado(self):
        return self._nombre

    def bloquear(self, evento, fechaHoraActual, usuario):
        raise NotImplementedError()

    # Caché opcional de instancias de estados para evitar crear múltiples
    # instancias sin necesidad. La clave es (nombre_normalizado, ambito).
    _state_cache = {}

    @classmethod
    def get_or_create_state(cls, nombre: str, ambito: str = None):
        """Devuelve una instancia compartida del estado indicado si existe en
        caché, o la crea mediante from_name y la guarda en caché.

        Esto satisface la necesidad de 'buscar si existe una instancia del
        estado y si no existe, crearla'. La clave incluye el ámbito para
        permitir diferentes instancias por contexto si fuera necesario.
        """
        key_name = (nombre or "").strip().lower().replace(" ", "").replace("-", "")
        key = (key_name, ambito)
        inst = cls._state_cache.get(key)
        if inst is not None:
            return inst
        # Crear mediante la fábrica y almacenar
        inst = cls.from_name(nombre, ambito)
        cls._state_cache[key] = inst
        return inst
    def rechazar(self, evento, fechaHoraActual, usuario):
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

<<<<<<< Updated upstream
    def esAutoDetectado(self):
        """Predicado por defecto: los estados concretos pueden sobrescribirlo.

        Esto permite al código cliente (por ejemplo, GestorRevisionManual) invocar
    `estado.esAutoDetectado()` respetando el patrón State y la polimorfía.
        """
        return False

    def esAutoConfirmado(self):
        """Indica si el estado es 'AutoConfirmado'. Sobrescribir en subclases."""
        return False

    def esBloqueado(self):
        """Indica si el estado representa un bloqueo para revisión."""
        return False

    def esRechazado(self):
        return False

    def esConfirmadoPorPersonal(self):
        return False

    def esDerivado(self):
        return False

    def esSinRevision(self):
        return False

    def esPendienteDeRevision(self):
        return False

    def esPendienteDeCierre(self):
        return False

    def esCerrado(self):
        return False

=======
        def esAutoDetectado(self):
                """
                Indica si este estado representa 'Auto-detectado'.

                Lógica:
                - Si el estado tiene un nombre explícito (`getNombreEstado()`), lo normaliza
                    y compara con la forma canonical 'autodetectado'.
                - Si no hay nombre, hace fallback comprobando el nombre de la clase
                    (por ejemplo `AutoDetectado`).
                """
                nombre = self.getNombreEstado()
                if nombre:
                        n = nombre.strip().lower().replace(" ", "").replace("-", "")
                        return n == "autodetectado"
                # Fallback por nombre de la clase (por ejemplo AutoDetectado)
                return self.__class__.__name__.lower() in ("autodetectado", "autodetect")
    
>>>>>>> Stashed changes
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

        if ambito is not None and ambito != 'EventoSismico':
            return Estado(nombre, ambito)

        raise ValueError(f"Estado desconocido: '{nombre}'")


def _es_ambito_evento_sismico(ambito):
    """Método auxiliar para identificar el ámbito de evento sismico"""
    return ambito == "EventoSismico"

