import datetime as _dt
import passlib.hash as _hash
import database as _database
from base import Base

import sqlalchemy as _sql
import sqlalchemy.orm as _orm

class Eventos(Base):
    __tablename__= "BLC_EVENTOS_CREACION"
    id_evento = _sql.Column(_sql.Integer, primary_key=True, index=True)
    fecha_creacion = _sql.Column(_sql.DateTime, default=_dt.datetime.now(_dt.timezone.utc))
    fecha_ejecucion = _sql.Column(_sql.DateTime, default=None)
    fecha_finalizacion = _sql.Column(_sql.DateTime, default=None)
    usuario_creador = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_USUARIOS.id_usuario"))

    evento = _orm.relationship("EventosDefinicion", back_populates="eventos")
    
    asistente = _orm.relationship("EventoUsuario", back_populates="evento")
    recurso = _orm.relationship("EventoRecursos", back_populates="evento")
    invitado = _orm.relationship("EventoInvitados", back_populates="evento")

class EventosDefinicion(Base):
    __tablename__= "BLC_EVENTOS"
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS_CREACION.id_evento"), primary_key=True, index=True)
    nombre = _sql.Column(_sql.String)
    descripcion = _sql.Column(_sql.String)
    categoria = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_CATEGORIA.id_categoria"))
    hora_inicio = _sql.Column(_sql.DateTime, default=None)
    hora_fin = _sql.Column(_sql.DateTime, default=None)
    fecha = _sql.Column(_sql.DateTime, default=None)
    idioma = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_IDIOMAS.id_idioma"))
    privacidad = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_PRIVACIDAD.id_privacidad"))
    modalidad = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_MODALIDAD.id_modalidad"))
    url_evento = _sql.Column(_sql.String, default=None)
    direccion = _sql.Column(_sql.String, default=None)
    latitud = _sql.Column(_sql.Float, default=None)
    longitud = _sql.Column(_sql.Float, default=None)
    url_redireccion = _sql.Column(_sql.String, default=None)


    eventos = _orm.relationship("Eventos", back_populates="evento")
    categorias = _orm.relationship("EventosCategoria", back_populates="categoria")
    idiomas = _orm.relationship("EventosIdioma", back_populates="idioma")
    privacidades = _orm.relationship("EventosPrivacidad", back_populates="privacidad")
    modalidades = _orm.relationship("EventosModalidad", back_populates="modalidad")

    imagenes = _orm.relationship("EventosImagenes", back_populates="imagen")

    qrs_publicos = _orm.relationship("EventosQRPublicos", back_populates="qr_publico")

    parametros = _orm.relationship("EventosParametros", back_populates="parametro")

class EventosCategoria(Base):
    __tablename__ = "BLC_CATEGORIA"
    id_categoria = _sql.Column(_sql.Integer, primary_key=True, index=True)
    descripcion = _sql.Column(_sql.String)

    categoria = _orm.relationship("EventosDefinicion", back_populates="categorias")

class EventosIdioma(Base):
    __tablename__ = "BLC_IDIOMAS"
    id_idioma = _sql.Column(_sql.Integer, primary_key=True, index=True)
    descripcion = _sql.Column(_sql.String)

    idioma = _orm.relationship("EventosDefinicion", back_populates="idiomas")

class EventosPrivacidad(Base):
    __tablename__ = "BLC_PRIVACIDAD"
    id_privacidad = _sql.Column(_sql.Integer, primary_key=True, index=True)
    descripcion = _sql.Column(_sql.String)

    privacidad = _orm.relationship("EventosDefinicion", back_populates="privacidades")

class EventosModalidad(Base):
    __tablename__ = "BLC_MODALIDAD"
    id_modalidad = _sql.Column(_sql.Integer, primary_key=True, index=True)
    descripcion = _sql.Column(_sql.String)

    modalidad = _orm.relationship("EventosDefinicion", back_populates="modalidades")

class EventosImagenes(Base):
    __tablename__ = "BLC_IMAGENES"
    id_imagen = _sql.Column(_sql.Integer, primary_key=True, index=True)
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS.id_evento"))
    nombre = _sql.Column(_sql.String)
    path = _sql.Column(_sql.String)

    imagen = _orm.relationship("EventosDefinicion", back_populates="imagenes")

class EventosQRPublicos(Base):
    __tablename__ = "BLC_QR_PUBLICO"
    id_qr = _sql.Column(_sql.Integer, primary_key=True, index=True)
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS.id_evento"))
    path = _sql.Column(_sql.String)

    qr_publico = _orm.relationship("EventosDefinicion", back_populates="qrs_publicos")

class EventosParametros(Base):
    __tablename__ = "BLC_PARAMETROS"
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS.id_evento"), primary_key=True, index=True)
    id_parametro = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_PARAMETROS_DEFINICION.id_parametro"))

    parametro = _orm.relationship("EventosDefinicion", back_populates="parametros")
    parametros = _orm.relationship("EventosParametrosDefinicion", back_populates="parametro")

class EventosParametrosDefinicion(Base):
    __tablename__ = "BLC_PARAMETROS_DEFINICION"
    id_parametro = _sql.Column(_sql.Integer, primary_key=True, index=True)
    descripcion = _sql.Column(_sql.String)

    parametro = _orm.relationship("EventosParametros", back_populates="parametros")