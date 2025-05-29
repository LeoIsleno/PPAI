from .Modelos.EventoSismico import EventoSismico # Importa la clase EventoSismico
from .estado import Estado # Importa la clase Estado  

class PantallaRevisionManual:
    def __init__(self):
        self.__cboEventosSismicos = []  # Simula un ComboBox de eventos
        self.__lblDatosSismicos = ""   # Simula un Label para mostrar datos
        self.__opcionMapa = None
        self.__opcionModificacionDatos = None
        self.__opcionEvento = None
        self.__evento_seleccionado_id = None  # ID del evento seleccionado

    def habilitarPantalla(self):
        print("Pantalla de Revisión Manual habilitada.")


    def mostrarEventosSismicos(self, eventos: list[EventoSismico]):
        self.__cboEventosSismicos = eventos
        print("\n--- Eventos Sísmicos Disponibles para Revisión ---")
        if not self.__cboEventosSismicos:
            print("No hay eventos sísmicos disponibles.")
            return
        for evento in self.__cboEventosSismicos:
            print(f"ID: {evento.id_evento}, Fecha: {evento.getFechaHoraOcurrencia()}, Magnitud: {evento.getValorMagnitud()}, Auto-detectado: {evento.esAutoDetectado()}")
        print("---------------------------------------------------")

    def tomarSeleccionDeEventoSismico(self,id_evento: int):
        self.__evento_seleccionado_id = id_evento
        return self.__evento_seleccionado_id
    
    def mostrarDatosSismicos(self, evento: EventoSismico):
        self.__lblDatosSismicos = f"""
        --- Datos del Evento Sísmico (ID: {evento.id_evento}) ---
        Fecha y Hora: {evento.getFechaHoraOcurrencia()}
        Latitud Epicentro: {evento.getLatitudEpicentro()}
        Longitud Epicentro: {evento.getLongitudEpicentro()}
        Latitud Hipocentro: {evento.getLatitudHipocentro()}
        Longitud Hipocentro: {evento.getLongitudHipocentro()}
        Magnitud: {evento.getValorMagnitud()}
        Estado: {evento.obtenerEstadoActual().get_nombre()}
        ----------------------------------------------------
        """
        print(self.__lblDatosSismicos)

    def mostrarOpcionMapa(self):
        self.__opcionMapa = input("Ingrese la opción para el mapa: ")
        return self.__opcionMapa

    def tomarSeleccionDeOpcionMapa(self, opcion):
        self.__opcionMapa = opcion
        print(f"Opción de mapa seleccionada: {self.__opcionMapa}")

    def mostrarOpcionModificacionDatos(self):
        self.__opcionModificacionDatos = input("Ingrese la opción para la modificación de datos: ")
        return self.__opcionModificacionDatos

    def tomarOpcionModificacionDatos(self, opcion):
        self.__opcionModificacionDatos = opcion
        print(f"Opción de modificación de datos seleccionada: {self.__opcionModificacionDatos}")

    def pedirOpcionEvento(self):
        self.__opcionEvento = input("Ingrese la opción para el evento: ")
        return self.__opcionEvento

    def tomarSeleccionOpcionEvento(self, opcion):
        self.__opcionEvento = opcion
        print(f"Opción de evento seleccionada: {self.__opcionEvento}")

    def opRegistrarResultadoRevisionManual(self, evento: EventoSismico):
        print(f"Registrando resultado de revisión manual para el evento ID: {evento.id_evento}")
        # Aquí iría la lógica para registrar el resultado de la revisión