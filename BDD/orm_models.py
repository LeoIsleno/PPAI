from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)

    empleados = relationship('Empleado', back_populates='rol')


class Empleado(Base):
    __tablename__ = 'empleado'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    apellido = Column(String(200), nullable=False)
    mail = Column(String(200), nullable=False, unique=False)
    telefono = Column(String(100))
    rol_id = Column(Integer, ForeignKey('rol.id'))

    rol = relationship('Rol', back_populates='empleados')
    usuario = relationship('Usuario', back_populates='empleado', uselist=False)


class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), unique=True, nullable=False)
    contrasena = Column(String(200), nullable=False)
    fecha_alta = Column(DateTime)
    empleado_id = Column(Integer, ForeignKey('empleado.id'))

    empleado = relationship('Empleado', back_populates='usuario')

    def es_administrador_sismos(self):
        if not self.empleado or not self.empleado.rol:
            return False
        return self.empleado.rol.nombre == 'Administrador de Sismos'


class OrigenDeGeneracion(Base):
    __tablename__ = 'origen_de_generacion'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)

    eventos = relationship('EventoSismico', back_populates='origen')


class AlcanceSismo(Base):
    __tablename__ = 'alcance_sismo'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    descripcion = Column(Text)

    eventos = relationship('EventoSismico', back_populates='alcance')


class ClasificacionSismo(Base):
    __tablename__ = 'clasificacion_sismo'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    km_profundidad_desde = Column(Float)
    km_profundidad_hasta = Column(Float)

    eventos = relationship('EventoSismico', back_populates='clasificacion')


class MagnitudRichter(Base):
    __tablename__ = 'magnitud_richter'
    id = Column(Integer, primary_key=True)
    descripcion = Column(String(200))
    numero = Column(Float)

    eventos = relationship('EventoSismico', back_populates='magnitud')


class EventoSismico(Base):
    __tablename__ = 'evento_sismico'
    id = Column(Integer, primary_key=True)
    fecha_hora_ocurrencia = Column(DateTime)
    fecha_hora_fin = Column(DateTime)
    latitud_epicentro = Column(Float)
    longitud_epicentro = Column(Float)
    latitud_hipocentro = Column(Float)
    longitud_hipocentro = Column(Float)
    magnitud_id = Column(Integer, ForeignKey('magnitud_richter.id'))
    origen_id = Column(Integer, ForeignKey('origen_de_generacion.id'))
    alcance_id = Column(Integer, ForeignKey('alcance_sismo.id'))
    clasificacion_id = Column(Integer, ForeignKey('clasificacion_sismo.id'))
    estado_actual_nombre = Column(String(200))
    estado_actual_ambito = Column(String(200))

    origen = relationship('OrigenDeGeneracion', back_populates='eventos')
    alcance = relationship('AlcanceSismo', back_populates='eventos')
    clasificacion = relationship('ClasificacionSismo', back_populates='eventos')
    magnitud = relationship('MagnitudRichter', back_populates='eventos')

    serie_temporal = relationship('SerieTemporal', back_populates='evento', cascade='all, delete-orphan')
    cambios_estado = relationship('CambioEstado', back_populates='evento', cascade='all, delete-orphan')


class CambioEstado(Base):
    __tablename__ = 'cambio_estado'
    id = Column(Integer, primary_key=True)
    fecha_hora_inicio = Column(DateTime)
    fecha_hora_fin = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    evento_id = Column(Integer, ForeignKey('evento_sismico.id'))
    estado_nombre = Column(String(200))
    estado_ambito = Column(String(200))
    
    usuario = relationship('Usuario')
    evento = relationship('EventoSismico', back_populates='cambios_estado')

    def es_estado_actual(self):
        return self.fecha_hora_fin is None


class TipoDeDato(Base):
    __tablename__ = 'tipo_de_dato'
    id = Column(Integer, primary_key=True)
    denominacion = Column(String(200))
    nombre_unidad_medida = Column(String(200))
    valor_umbral = Column(Float)

    detalles = relationship('DetalleMuestraSismica', back_populates='tipo_de_dato')


class MuestraSismica(Base):
    __tablename__ = 'muestra_sismica'
    id = Column(Integer, primary_key=True)
    fecha_hora_muestra = Column(DateTime)
    serie_id = Column(Integer, ForeignKey('serie_temporal.id'))

    detalles = relationship('DetalleMuestraSismica', back_populates='muestra', cascade='all, delete-orphan')
    serie = relationship('SerieTemporal', back_populates='muestras')


class DetalleMuestraSismica(Base):
    __tablename__ = 'detalle_muestra_sismica'
    id = Column(Integer, primary_key=True)
    valor = Column(Float)
    tipo_de_dato_id = Column(Integer, ForeignKey('tipo_de_dato.id'))
    muestra_id = Column(Integer, ForeignKey('muestra_sismica.id'))

    tipo_de_dato = relationship('TipoDeDato', back_populates='detalles')
    muestra = relationship('MuestraSismica', back_populates='detalles')


class SerieTemporal(Base):
    __tablename__ = 'serie_temporal'
    id = Column(Integer, primary_key=True)
    fecha_hora_inicio_registro_muestras = Column(DateTime)
    fecha_hora_registro = Column(DateTime)
    frecuencia_muestreo = Column(Float)
    condicion_alarma = Column(Boolean)
    evento_id = Column(Integer, ForeignKey('evento_sismico.id'))
    sismografo_id = Column(Integer, ForeignKey('sismografo.id'))
    estado_nombre = Column(String(200))
    estado_ambito = Column(String(200))
    muestras = relationship('MuestraSismica', back_populates='serie', cascade='all, delete-orphan')
    evento = relationship('EventoSismico', back_populates='serie_temporal')
    sismografo = relationship('Sismografo', back_populates='series_temporales')


class Sismografo(Base):
    __tablename__ = 'sismografo'
    id = Column(Integer, primary_key=True)
    identificador_sismografo = Column(String(200))
    nro_serie = Column(String(200))
    fecha_adquisicion = Column(DateTime)
    estacion_id = Column(Integer, ForeignKey('estacion_sismologica.id'))

    estacion = relationship('EstacionSismologica', back_populates='sismografos')
    series_temporales = relationship('SerieTemporal', back_populates='sismografo', cascade='all, delete-orphan')


class EstacionSismologica(Base):
    __tablename__ = 'estacion_sismologica'
    id = Column(Integer, primary_key=True)
    codigo_estacion = Column(String(200))
    nombre = Column(String(200))
    latitud = Column(Float)
    longitud = Column(Float)
    documento_certificacion_adq = Column(Text)
    fecha_solicitud_certificacion = Column(DateTime)
    nro_certificacion_adquisicion = Column(String(200))

    sismografos = relationship('Sismografo', back_populates='estacion')


class Sesion(Base):
    __tablename__ = 'sesion'
    id = Column(Integer, primary_key=True)
    fecha_hora_desde = Column(DateTime)
    fecha_hora_hasta = Column(DateTime)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))

    usuario = relationship('Usuario')


class EstadoAutoDetectado(Base):
    __tablename__ = 'estado_auto_detectado'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoAutoConfirmado(Base):
    __tablename__ = 'estado_auto_confirmado'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoPendienteDeCierre(Base):
    __tablename__ = 'estado_pendiente_de_cierre'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoDerivado(Base):
    __tablename__ = 'estado_derivado'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoConfirmadoPorPersonal(Base):
    __tablename__ = 'estado_confirmado_por_personal'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoCerrado(Base):
    __tablename__ = 'estado_cerrado'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoRechazado(Base):
    __tablename__ = 'estado_rechazado'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoBloqueadoEnRevision(Base):
    __tablename__ = 'estado_bloqueado_en_revision'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoPendienteDeRevision(Base):
    __tablename__ = 'estado_pendiente_de_revision'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))


class EstadoSinRevision(Base):
    __tablename__ = 'estado_sin_revision'
    id = Column(Integer, primary_key=True)
    nombre_estado = Column(String(200), nullable=False)
    ambito = Column(String(200))
