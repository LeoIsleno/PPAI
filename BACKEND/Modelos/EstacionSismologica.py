class EstacionSismologica:
    def __init__(self, codigoEstacion, nombre, latitud, longitud, documentoCertificacionAdq, fechaSolicitudCertificacion, nroCertificacionAdquisicion):
        self.__codigoEstacion = codigoEstacion
        self.__nombre = nombre
        self.__latitud = latitud
        self.__longitud = longitud
        self.__documentoCertificacionAdq = documentoCertificacionAdq
        self.__fechaSolicitudCertificacion = fechaSolicitudCertificacion
        self.__nroCertificacionAdquisicion = nroCertificacionAdquisicion

# Codigo de la estacion
    def getCodigoEstacion(self):
        return self.__codigoEstacion

    def setCodigoEstacion(self, codigoEstacion):
        self.__codigoEstacion = codigoEstacion

# Nombre
    def getNombre(self):
        return self.__nombre

    def setNombre(self, nombre):
        self.__nombre = nombre

# Latitud
    def getLatitud(self):
        return self.__latitud

    def setLatitud(self, latitud):
        self.__latitud = latitud

# Longitud
    def getLongitud(self):
        return self.__longitud

    def setLongitud(self, longitud):
        self.__longitud = longitud

# Documento de certificacion de adquisicion
    def getDocumentoCertificacionAdq(self):
        return self.__documentoCertificacionAdq

    def setDocumentoCertificacionAdq(self, doc):
        self.__documentoCertificacionAdq = doc

# Fecha de solicitud de certificacion
    def getFechaSolicitudCertificacion(self):
        return self.__fechaSolicitudCertificacion

    def setFechaSolicitudCertificacion(self, fecha):
        self.__fechaSolicitudCertificacion = fecha

# Numero de certificacion de adquisicion
    def getNroCertificacionAdquisicion(self):
        return self.__nroCertificacionAdquisicion

    def setNroCertificacionAdquisicion(self, nro):
        self.__nroCertificacionAdquisicion = nro

