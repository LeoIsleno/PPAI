from Modelos.evento_sismico import EventoSismico
from Modelos.estado import Estado
from Modelos.clasificacion_sismo import ClasificacionSismo
from Modelos.origen_de_generacion import OrigenDeGeneracion
from Modelos.alcance_sismo import AlcanceSismo
from Modelos.serie_temporal import SerieTemporal
from Modelos.muestra_sismica import MuestraSismica
from Modelos.detalle_muestra_sismica import DetalleMuestraSismica
from Modelos.tipo_de_dato import TipoDeDato
from Modelos.cambio_estado import CambioEstado
from datetime import datetime, timedelta

def crear_eventos_sismicos():
    # Crear estados
    estado_auto_detectado = Estado("Auto-detectado", "EventoSismico")
    estado_normal = Estado("Normal", "EventoSismico")
    estado_bloqueado = Estado("BloqueadoEnRevision", "EventoSismico")
    estado_rechazado = Estado("Rechazado", "EventoSismico")

    # Crear clasificaciones
    clasificacion_superficial = ClasificacionSismo("Superficial", 0, 70)
    clasificacion_intermedio = ClasificacionSismo("Intermedio", 71, 300)
    clasificacion_profundo = ClasificacionSismo("Profundo", 301, 700)

    # Crear orígenes de generación
    origen_natural = OrigenDeGeneracion("Natural", "Sismo de origen tectónico natural")
    origen_artificial = OrigenDeGeneracion("Artificial", "Sismo provocado por actividad humana")

    # Crear alcances
    alcance_local = AlcanceSismo("Afecta área local", "Local")
    alcance_regional = AlcanceSismo("Afecta área regional", "Regional")
    alcance_nacional = AlcanceSismo("Afecta área nacional", "Nacional")

    # Crear tipos de datos para muestras
    tipo_aceleracion = TipoDeDato("Aceleración", "m/s²", 9.8)
    tipo_velocidad = TipoDeDato("Velocidad", "m/s", 5.0)
    tipo_desplazamiento = TipoDeDato("Desplazamiento", "m", 0.1)

    # Lista para almacenar todos los eventos
    eventos = []

    # Crear múltiples eventos con datos completos
    for i in range(8):  # Crear 8 eventos
        # Crear detalles de muestras
        detalle_acel = DetalleMuestraSismica(round(2.5 + i * 0.5, 2), tipo_aceleracion)
        detalle_vel = DetalleMuestraSismica(round(1.2 + i * 0.3, 2), tipo_velocidad)
        detalle_desp = DetalleMuestraSismica(round(0.05 + i * 0.01, 2), tipo_desplazamiento)

        # Crear muestras sísmicas
        muestra1 = MuestraSismica(datetime.now() - timedelta(minutes=30), detalle_acel)
        muestra2 = MuestraSismica(datetime.now() - timedelta(minutes=20), detalle_vel)
        muestra3 = MuestraSismica(datetime.now() - timedelta(minutes=10), detalle_desp)

        # Crear serie temporal
        serie_temporal = SerieTemporal(
            datetime.now() - timedelta(minutes=30),
            datetime.now(),
            100,  # frecuencia de muestreo
            False,  # condición de alarma
            muestra1
        )
        # Agregar más muestras a la serie
        serie_temporal.agregarMuestraSismica(muestra2)
        serie_temporal.agregarMuestraSismica(muestra3)

        # Crear cambios de estado
        cambios_estado = [
            CambioEstado(
                datetime.now() - timedelta(hours=2),
                estado_auto_detectado if i % 2 == 0 else estado_normal
            )
        ]

        # Crear el evento sísmico
        evento = EventoSismico(
            fechaHoraOcurrencia=datetime(2025, 5, 24 + i, 10 + i, 0, 0),
            latitudEpicentro=-31.5 - (i * 0.2),
            longitudEpicentro=-64.0 - (i * 0.2),
            latitudHipocentro=-31.4 - (i * 0.2),
            longitudHipocentro=-63.9 - (i * 0.2),
            valorMagnitud=round(3.5 + (i * 0.3), 1),
            origenGeneracion=origen_natural if i % 2 == 0 else origen_artificial,
            estadoActual=estado_auto_detectado if i % 2 == 0 else estado_normal,
            cambiosEstado=cambios_estado,
            clasificacion=clasificacion_superficial if i < 3 else (clasificacion_intermedio if i < 6 else clasificacion_profundo),
            alcanceSismo=alcance_local if i < 3 else (alcance_regional if i < 6 else alcance_nacional),
            serieTemporal=serie_temporal
        )
        eventos.append(evento)

    return eventos
