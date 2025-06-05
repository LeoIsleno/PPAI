# ListaEventosSismicos.py - Generador de eventos sísmicos de ejemplo para la aplicación
# Este archivo crea una lista de eventos sísmicos con datos realistas y estructura anidada.

from Modelos.EventoSismico import EventoSismico
from Modelos.Estado import Estado
from Modelos.ClasificacionSismo import ClasificacionSismo
from Modelos.OrigenDeGeneracion import OrigenDeGeneracion
from Modelos.AlcanceSismo import AlcanceSismo
from Modelos.SerieTemporal import SerieTemporal
from Modelos.MuestraSismica import MuestraSismica
from Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from Modelos.TipoDeDato import TipoDeDato
from Modelos.CambioEstado import CambioEstado
from datetime import datetime, timedelta
from random import randint, choice


class ListarEventosSismicos:
    def __init__(self):
        # Llamar a la función para crear los eventos sísmicos
        self.evento = self.crear_eventos_sismicos()

    # Función principal para crear una lista de eventos sísmicos de ejemplo
    @staticmethod
    def crear_eventos_sismicos(sismografos, usuario):
        # Crear estados posibles para los eventos
        estado_auto_detectado = Estado("Auto-detectado", "EventoSismico")
        estado_normal = Estado("Normal", "EventoSismico")
        estado_bloqueado = Estado("BloqueadoEnRevision", "EventoSismico")
        estado_rechazado = Estado("Rechazado", "EventoSismico")

        # Crear estados para series temporales (si corresponde)
        estado_serie_activa = Estado("Activa", "SerieTemporal")
        estado_serie_inactiva = Estado("Inactiva", "SerieTemporal")

        # Crear clasificaciones de profundidad
        clasificacion_superficial = ClasificacionSismo("Superficial", 0, 70)
        clasificacion_intermedio = ClasificacionSismo("Intermedio", 71, 300)
        clasificacion_profundo = ClasificacionSismo("Profundo", 301, 700)

        # Crear alcances posibles del sismo
        alcance_local = AlcanceSismo("Afecta área local", "Local")
        alcance_regional = AlcanceSismo("Afecta área regional", "Regional")
        alcance_nacional = AlcanceSismo("Afecta área nacional", "Nacional")
        # Lista de nombres de alcances para el frontend
        ALCANCES_SISMO = [alcance_local.getNombre(), alcance_regional.getNombre(), alcance_nacional.getNombre()]

        # Crear orígenes posibles del sismo
        origen_natural = OrigenDeGeneracion("Natural", "Sismo de origen tectónico natural")
        origen_artificial = OrigenDeGeneracion("Artificial", "Sismo provocado por actividad humana")
        # Lista de nombres de orígenes para el frontend
        ORIGENES_GENERACION = [origen_natural.getNombre(), origen_artificial.getNombre()]

        # Crear tipos de datos para los detalles de las muestras
        tipo_aceleracion = TipoDeDato("Aceleración", "m/s²", 9.8)
        tipo_velocidad = TipoDeDato("Velocidad", "m/s", 5.0)
        tipo_desplazamiento = TipoDeDato("Desplazamiento", "m", 0.1)

        # Función auxiliar para formatear valores numéricos
        def fmt(val, dec=2, sufijo=None):
            if isinstance(val, float):
                val = round(val, dec)
            return f"{val}{' ' + sufijo if sufijo else ''}"

        eventos = []  # Lista para almacenar todos los eventos generados

        # Crear 15 eventos sísmicos con datos variados y realistas
        for i in range(15):
            # Variar la fecha y la ubicación para que cada evento sea único
            base_fecha = datetime(2025, 2, 21, 19, 5, 41) + timedelta(hours=i)  # Cada evento una hora después
            lat_epicentro = -31.5 + (i * 0.1)  # Variar latitud
            long_epicentro = -64.0 + (i * 0.1)  # Variar longitud
            lat_hipocentro = -31.4 + (i * 0.1)
            long_hipocentro = -63.9 + (i * 0.1)
            magnitud = round(5.0 + (i % 5) * 0.3, 2)  # Magnitud variable entre 5.0 y 6.2
            # Cantidad aleatoria de series temporales por evento (1 a 3)
            
            # Cambios de estado del evento (historial)
            cambios_estado = [
                CambioEstado(
                    base_fecha,
                    estado_auto_detectado if i % 2 == 0 else estado_normal,
                    usuario
                )
            ]
            # Crear el evento sísmico con todos sus datos y series
            evento = EventoSismico(
                fechaHoraOcurrencia=base_fecha,
                latitudEpicentro=lat_epicentro,
                longitudEpicentro=long_epicentro,
                latitudHipocentro=lat_hipocentro,
                longitudHipocentro=long_hipocentro,
                valorMagnitud=magnitud,
                origenGeneracion=origen_natural if i % 2 == 0 else origen_artificial,
                estadoActual=estado_auto_detectado if i % 2 == 0 else estado_normal,
                cambiosEstado=cambios_estado,
                clasificacion=clasificacion_superficial,
                alcanceSismo=alcance_local,
                serieTemporal=sismografos[i].getSerieTemporal() + sismografos[i+1].getSerieTemporal() if i < len(sismografos) else [],
            )
            # Asignar un id_evento basado en la instancia en memoria
            evento.id_evento = id(evento)
            eventos.append(evento)

        return eventos

    @staticmethod
    def obtener_alcances():
        # Devuelve una lista de objetos AlcanceSismo
        return [
            AlcanceSismo("Afecta área local", "Local"),
            AlcanceSismo("Afecta área regional", "Regional"),
            AlcanceSismo("Afecta área nacional", "Nacional")
        ]

    @staticmethod
    def obtener_origenes():
        # Devuelve una lista de objetos OrigenDeGeneracion
        return [
            OrigenDeGeneracion("Natural", "Sismo de origen tectónico natural"),
            OrigenDeGeneracion("Artificial", "Sismo provocado por actividad humana")
        ]

    def obtener_estados():
        # Devuelve una lista de objetos Estado
        return [
            Estado("Auto-detectado", "EventoSismico"),
            Estado("BloqueadoEnRevision", "EventoSismico"),
            Estado("Rechazado", "EventoSismico"),
            Estado("Aceptado", "EventoSismico"),
            Estado("EnRevision", "EventoSismico"),
            Estado("PendienteDeRevision", "EventoSismico")
        ]





