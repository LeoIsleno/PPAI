from ..Estado import Estado


class BloqueadoEnRevision(Estado):
    """Estado BloqueadoEnRevision: evento bloqueado para revisión manual."""

    def __init__(self, ambito=None):
        super().__init__("Bloqueado en Revisión", ambito)

    def getNombreEstado(self):
        return "Bloqueado en Revisión"

    def rechazar(self, evento_sismico, fecha_hora_actual, usuario):
        # 1. Finalizar el estado actual
        cambio_estado_actual = evento_sismico.obtenerCambioEstadoActual()
        if cambio_estado_actual:
            try:
                cambio_estado_actual.setFechaHoraFin(fecha_hora_actual)
            except (AttributeError, TypeError):
                pass

        # 2. Crear el próximo estado
        proximo_estado = self.crearProximoEstado("Rechazado")

        # 3. Crear el nuevo cambio de estado
        nuevo_cambio_estado = self.crearCambioEstado(proximo_estado, fecha_hora_actual, usuario)
        
        # 4. Actualizar el evento sísmico
        evento_sismico.setEstadoActual(proximo_estado)
        evento_sismico.setCambioEstadoActual(nuevo_cambio_estado)
        evento_sismico.getCambiosEstado().append(nuevo_cambio_estado)
        
        return nuevo_cambio_estado

    def confirmar(self, evento_sismico, fecha_hora_actual, usuario):
        cambio_estado_actual = evento_sismico.obtenerCambioEstadoActual()
        if cambio_estado_actual:
            try:
                cambio_estado_actual.setFechaHoraFin(fecha_hora_actual)
            except (AttributeError, TypeError):
                pass

        proximo_estado = self.crearProximoEstado("ConfirmadoPorPersonal")
        nuevo_cambio_estado = self.crearCambioEstado(proximo_estado, fecha_hora_actual, usuario)
        
        evento_sismico.setEstadoActual(proximo_estado)
        evento_sismico.setCambioEstadoActual(nuevo_cambio_estado)
        evento_sismico.getCambiosEstado().append(nuevo_cambio_estado)
        
        return nuevo_cambio_estado

    def derivar(self, evento_sismico, fecha_hora_actual, usuario):
        cambio_estado_actual = evento_sismico.obtenerCambioEstadoActual()
        if cambio_estado_actual:
            try:
                cambio_estado_actual.setFechaHoraFin(fecha_hora_actual)
            except (AttributeError, TypeError):
                pass

        proximo_estado = self.crearProximoEstado("Derivado")
        nuevo_cambio_estado = self.crearCambioEstado(proximo_estado, fecha_hora_actual, usuario)
        
        evento_sismico.setEstadoActual(proximo_estado)
        evento_sismico.setCambioEstadoActual(nuevo_cambio_estado)
        evento_sismico.getCambiosEstado().append(nuevo_cambio_estado)
        
        return nuevo_cambio_estado

    def crearProximoEstado(self, tipo_estado):
        # Importar localmente para evitar problemas de import circular y
        # permitir que cada estado se resuelva en tiempo de ejecución.
        if tipo_estado == "Rechazado":
            from .Rechazado import Rechazado
            return Rechazado("Rechazado", "Evento Sismico")
        elif tipo_estado == "ConfirmadoPorPersonal":
            from .ConfirmadoPorPersonal import ConfirmadoPorPersonal
            return ConfirmadoPorPersonal("Confirmado por Personal", "Evento Sismico")
        elif tipo_estado == "Derivado":
            from .Derivado import Derivado
            return Derivado("Derivado", "Evento Sismico")
        return None

    def crearCambioEstado(self, estado, fecha_hora_inicio, usuario):
        # Importar CambioEstado localmente para evitar import circular
        from ..CambioEstado import CambioEstado
        return CambioEstado(fecha_hora_inicio, estado, usuario)
