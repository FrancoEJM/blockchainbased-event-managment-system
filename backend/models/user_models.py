import datetime as _dt
import passlib.hash as _hash
import database as _database
from base import Base

import sqlalchemy as _sql
import sqlalchemy.orm as _orm

class Usuario(Base):
    __tablename__= "BLC_USUARIOS"
    id_usuario = _sql.Column(_sql.Integer, primary_key=True, index=True)
    correo_electronico = _sql.Column(_sql.String, unique=True, index=True)
    hash_contrasena = _sql.Column(_sql.String)
    fecha_registro = _sql.Column(_sql.DateTime, default=_dt.datetime.now(_dt.timezone.utc))
    nombre = _sql.Column(_sql.String)
    apellido = _sql.Column(_sql.String)
    fecha_nacimiento = _sql.Column(_sql.DateTime, default=None)
    genero = _sql.Column(_sql.Integer, _sql.ForeignKey("BLC_GENERO.id_genero"), default=0)
    imagen = _sql.Column(_sql.String, default="")
    habilitado = _sql.Column(_sql.Boolean, default=True)
    direccion = _sql.Column(_sql.String, default="")
    comuna = _sql.Column(_sql.String, default="")
    region = _sql.Column(_sql.String, default="")
    nacionalidad = _sql.Column(_sql.String, default="")

    generos = _orm.relationship("Genero", back_populates="propietario")

    asistente = _orm.relationship("EventoUsuario", back_populates="usuario")
    recurso = _orm.relationship("EventoRecursos", back_populates="usuario")
    invitado = _orm.relationship("EventoInvitados", back_populates="usuario")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hash_contrasena)

class Genero(Base):
    __tablename__= "BLC_GENERO"
    id_genero = _sql.Column(_sql.Integer, primary_key=True, index=True)
    descripcion = _sql.Column(_sql.String)

    propietario = _orm.relationship("Usuario", back_populates="generos")