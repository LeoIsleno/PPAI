# ListaEventosSismicos.py - Generador de eventos sísmicos de ejemplo para la aplicación
# Este archivo crea una lista de eventos sísmicos con datos realistas y estructura anidada.

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
from random import randint, choice

# Función principal para crear una lista de eventos sísmicos de ejemplo
def crear_eventos_sismicos():
    # Crear estados posibles para los eventos
    estado_auto_detectado = Estado("Auto-detectado", "EventoSismico")
    estado_normal = Estado("Normal", "EventoSismico")
    estado_bloqueado = Estado("BloqueadoEnRevision", "EventoSismico")
    estado_rechazado = Estado("Rechazado", "EventoSismico")

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
        num_series = randint(1, 3)
        series_temporales = []
        for s in range(num_series):
            # Cantidad aleatoria de muestras por serie (2 a 4)
            num_muestras = randint(2, 4)
            muestras = []
            for m in range(num_muestras):
                # Cantidad aleatoria de detalles por muestra (2 o 3)
                num_detalles = randint(2, 3)
                detalles = []
                # Siempre incluir los tres tipos, pero puede faltar uno aleatoriamente
                tipos = [
                    ('Velocidad de onda', 'Km/seg', 'Km/seg', ['7', '7.02', '6.99', '7.1']),
                    ('Frecuencia de onda', 'Hz', 'Hz', ['10', '10.01', '9.98', '10.2']),
                    ('Longitud', 'km/ciclo', 'km/ciclo', ['0.7', '0.69', '0.71', '0.68'])
                ]
                tipos_detalle = tipos.copy()
                # Eliminar uno aleatoriamente si solo se quieren 2 detalles
                if num_detalles == 2:
                    tipos_detalle.pop(randint(0,2))
                for tipo, unidad, sufijo, valores in tipos_detalle:
                    valor = choice(valores)
                    # Crear el detalle de la muestra según el tipo
                    if tipo == 'Velocidad de onda':
                        detalles.append(DetalleMuestraSismica(f'{valor} {sufijo}', TipoDeDato(tipo, unidad, 10)))
                    elif tipo == 'Frecuencia de onda':
                        detalles.append(DetalleMuestraSismica(f'{valor} {sufijo}', TipoDeDato(tipo, unidad, 20)))
                    elif tipo == 'Longitud':
                        detalles.append(DetalleMuestraSismica(f'{valor} {sufijo}', TipoDeDato(tipo, unidad, 1)))
                # Fecha de la muestra (espaciada 5 minutos entre cada una)
                muestra_fecha = base_fecha.replace(minute=5 + m*5)
                muestras.append(MuestraSismica(muestra_fecha, detalles))
            # Crear la serie temporal con sus muestras
            serie_temporal = SerieTemporal(
                base_fecha,
                base_fecha,
                50 + 10*s,  # frecuencia de muestreo
                bool(s % 2),
                muestras[0]
            )
            for muestra in muestras[1:]:
                serie_temporal.agregarMuestraSismica(muestra)
            series_temporales.append(serie_temporal)
        # Cambios de estado del evento (historial)
        cambios_estado = [
            CambioEstado(
                base_fecha,
                estado_auto_detectado if i % 2 == 0 else estado_normal
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
            serieTemporal=series_temporales
        )
        # Asignar un id_evento basado en la instancia en memoria
        evento.id_evento = id(evento)
        eventos.append(evento)

    return eventos, ALCANCES_SISMO, ORIGENES_GENERACION
