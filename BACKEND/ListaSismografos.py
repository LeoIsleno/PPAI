from ListaEventosSismicos import ListarEventosSismicos as listaEventos
from Modelos.Sismografo import Sismografo
from Modelos.EstacionSismologica import EstacionSismologica

# Supongamos que lista_eventos_sismicos es una lista de eventos sismicos ya creada en listaEventosSismicos.py
class ListaSismografos:
    def __init__(self):
        # Llamar a la función para crear los sismografos
        self.sismografos = self.crearSismografos()

    @staticmethod
    def crearSismografos():
        # Crear una instancia de ListarEventosSismicos para obtener los eventos sismicos
        sismografos = []
        eventos = listaEventos.crear_eventos_sismicos()
        estacion1 = EstacionSismologica(
            codigoEstacion="EST001",
            nombre="Estación Central",
            latitud=34.05,
            longitud=-118.25,
            documentoCertificacionAdq="certificacion.pdf",
            fechaSolicitudCertificacion="2023-01-01",
            nroCertificacionAdquisicion="CERT12345" 
        )

        sismografo1 = Sismografo(
            identificadorSismografo=1,
            nroSerie="SISMO123",
            fechaAdquisicion="2023-10-01",
            estacionSismologica=estacion1,
            serieTemporal=eventos[0].getSerieTemporal()[0]  # Asumiendo que cada evento tiene al menos una serie temporal
        )
        estacion2 = EstacionSismologica(
            codigoEstacion="EST002",
            nombre="Estación Norte",
            latitud=35.00,
            longitud=-119.00,
            documentoCertificacionAdq="certificacion2.pdf",
            fechaSolicitudCertificacion="2023-01-02",
            nroCertificacionAdquisicion="CERT12346"
        )
        sismografo2 = Sismografo(
            identificadorSismografo=2,
            nroSerie="SISMO456",
            fechaAdquisicion="2023-10-02",
            estacionSismologica=estacion2,
            serieTemporal=eventos[1].getSerieTemporal()[0]
        )

        estacion3 = EstacionSismologica(
            codigoEstacion="EST003",
            nombre="Estación Sur",
            latitud=33.50,
            longitud=-117.80,
            documentoCertificacionAdq="certificacion3.pdf",
            fechaSolicitudCertificacion="2023-01-03",
            nroCertificacionAdquisicion="CERT12347"
        )
        sismografo3 = Sismografo(
            identificadorSismografo=3,
            nroSerie="SISMO789",
            fechaAdquisicion="2023-10-03",
            estacionSismologica=estacion3,
            serieTemporal=eventos[2].getSerieTemporal()[0]
        )

        estacion4 = EstacionSismologica(
            codigoEstacion="EST004",
            nombre="Estación Este",
            latitud=34.20,
            longitud=-118.00,
            documentoCertificacionAdq="certificacion4.pdf",
            fechaSolicitudCertificacion="2023-01-04",
            nroCertificacionAdquisicion="CERT12348"
        )
        sismografo4 = Sismografo(
            identificadorSismografo=4,
            nroSerie="SISMO101",
            fechaAdquisicion="2023-10-04",
            estacionSismologica=estacion4,
            serieTemporal=eventos[3].getSerieTemporal()[0]
        )

        estacion5 = EstacionSismologica(
            codigoEstacion="EST005",
            nombre="Estación Oeste",
            latitud=34.10,
            longitud=-118.50,
            documentoCertificacionAdq="certificacion5.pdf",
            fechaSolicitudCertificacion="2023-01-05",
            nroCertificacionAdquisicion="CERT12349"
        )
        sismografo5 = Sismografo(
            identificadorSismografo=5,
            nroSerie="SISMO102",
            fechaAdquisicion="2023-10-05",
            estacionSismologica=estacion5,
            serieTemporal=eventos[4].getSerieTemporal()[0]
        )


        sismografos.append(sismografo1)
        sismografos.append(sismografo2)
        sismografos.append(sismografo3)
        sismografos.append(sismografo4)
        sismografos.append(sismografo5)
        return sismografos