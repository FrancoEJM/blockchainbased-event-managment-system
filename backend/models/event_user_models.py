import datetime as _dt
import passlib.hash as _hash
import database as _database
from base import Base

import sqlalchemy as _sql
import sqlalchemy.orm as _orm

class EventoUsuario(Base):
    __tablename__= "BLC_EVENTO_USUARIO"
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS_CREACION.id_evento"), primary_key=True, index=True)
    id_usuario = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_USUARIOS.id_usuario"), primary_key=True, index=True)
    invitado = _sql.Column(_sql.Boolean, default=False)
    correo_electronico = _sql.Column(_sql.String)
    fecha_inscripcion = _sql.Column(_sql.DateTime, default=_dt.datetime.now(_dt.timezone.utc))
    fecha_baja = _sql.Column(_sql.DateTime, default=None)
    fecha_arribo = _sql.Column(_sql.DateTime, default=None)

    evento = _orm.relationship("Eventos", back_populates="inscripcion")
    usuario = _orm.relationship("Usuario", back_populates="inscripcion")

class EventoRecursos(Base):
    __tablename__= "BLC_EVENTOS_RECURSOS"
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS_CREACION.id_evento"), primary_key=True, index=True)
    id_usuario = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_USUARIOS.id_usuario"), primary_key=True, index=True)
    path_qr = _sql.Column(_sql.String)
    validado = _sql.Column(_sql.Boolean, default=False)
    fecha_validacion = _sql.Column(_sql.DateTime, default=None)

    evento = _orm.relationship("Eventos", back_populates="recurso")
    usuario = _orm.relationship("Usuario", back_populates="recurso")

class EventoInvitados(Base):
    __tablename__= "BLC_EVENTOS_INVITADOS"
    id_evento = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_EVENTOS_CREACION.id_evento"), primary_key=True, index=True)
    id_usuario = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_USUARIOS.id_usuario"), primary_key=True, index=True)
    correo_electronico = _sql.Column(_sql.String, primary_key=True)
    inscrito = _sql.Column(_sql.Boolean, default=False)
    fecha_invitacion = _sql.Column(_sql.DateTime, default=_dt.datetime.now(_dt.timezone.utc))

    evento = _orm.relationship("Eventos", back_populates="invitado")
    usuario = _orm.relationship("Usuario", back_populates="invitado")