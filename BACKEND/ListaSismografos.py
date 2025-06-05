from ListaEventosSismicos import ListarEventosSismicos as listaEventos
from Modelos.Sismografo import Sismografo
from Modelos.EstacionSismologica import EstacionSismologica
from Modelos.MuestraSismica import MuestraSismica
from Modelos.DetalleMuestraSismica import DetalleMuestraSismica
from Modelos.TipoDeDato import TipoDeDato
from Modelos.SerieTemporal import SerieTemporal
from Modelos.CambioEstado import CambioEstado
from Modelos.Estado import Estado
from random import randint, choice
from datetime import datetime, timedelta

# Supongamos que lista_eventos_sismicos es una lista de eventos sismicos ya creada en listaEventosSismicos.py
class ListaSismografos:
    def __init__(self):
        # Llamar a la función para crear los sismografos
        self.sismografos = self.crearSismografos()

    @staticmethod
    def crear_sismografos(usuario):
        # Crear una instancia de ListarEventosSismicos para obtener los eventos sismicos
        sismografos = []
        estado_serie_activa = Estado("Activa", "SerieTemporal")
        

        for i in range(1, 20):  # Cambia 16 por la cantidad que desees +1

            series_temporales = []
            base_fecha = datetime(2025, 2, 21, 19, 5, 41) + timedelta(hours=i)
            num_series = randint(2, 5)
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
                # Cambios de estado para la serie temporal
                cambios_estado_serie = [
                    CambioEstado(
                        base_fecha,
                        estado_serie_activa,
                        usuario
                    )
                ]
                # Crear la serie temporal con sus muestras, estado y cambios de estado
                serie_temporal = SerieTemporal(
                    base_fecha,
                    base_fecha,
                    50 + 10*s,  # frecuencia de muestreo
                    bool(s % 2),
                    muestras[0],
                    estado_serie_activa,
                    cambios_estado_serie
                )
                for muestra in muestras[1:]:
                    serie_temporal.agregarMuestraSismica(muestra)
                series_temporales.append(serie_temporal)

            estacion = EstacionSismologica(
            codigoEstacion=f"EST{str(i).zfill(3)}",
            nombre=f"Estación {i}",
            latitud=34.0 + i * 0.1,
            longitud=-118.0 - i * 0.1,
            documentoCertificacionAdq=f"certificacion{i}.pdf",
            fechaSolicitudCertificacion=f"2023-01-{str(i).zfill(2)}",
            nroCertificacionAdquisicion=f"CERT123{44 + i}"
            )
            # Usa eventos de forma cíclica si hay menos eventos que estaciones
            sismografo = Sismografo(
            identificadorSismografo=i,
            nroSerie=f"SISMO{str(100 + i)}",
            fechaAdquisicion=f"2023-10-{str(i).zfill(2)}",
            estacionSismologica=estacion,
            serieTemporal = series_temporales
            )
            sismografos.append(sismografo)
        return sismografos
