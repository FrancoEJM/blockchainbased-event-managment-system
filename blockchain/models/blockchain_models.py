import datetime as _dt
from base import Base

import sqlalchemy as _sql


class BLOQUES(Base):
    __tablename__ = "blc_bloque"
    id_bloque = _sql.Column(_sql.Integer, primary_key=True, index=True)
    fecha_inicio = _sql.Column(_sql.DateTime)
    fecha_fin = _sql.Column(_sql.DateTime)
    id_evento = _sql.Column(_sql.Integer)
    org = _sql.Column(_sql.String)
    creador = _sql.Column(_sql.Integer)
    path = _sql.Column(_sql.String)
    timestamp = _sql.Column(_sql.Date)
    numero_bloque = _sql.Column(_sql.Integer)

    def to_dict(self):
        return {
            "id_bloque": self.id_bloque,
            "fecha_inicio": self.fecha_inicio.isoformat()
            if self.fecha_inicio
            else None,
            "fecha_fin": self.fecha_fin.isoformat() if self.fecha_fin else None,
            "id_evento": self.id_evento,
            "org": self.org,
            "creador": self.creador,
            "path": self.path,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "numero_bloque": self.numero_bloque,
        }


class NODOS(Base):
    __tablename__ = "blc_nodo"
    id_nodo = _sql.Column(_sql.Integer, primary_key=True, index=True)
    fecha_creacion = _sql.Column(
        _sql.DateTime, default=_dt.datetime.now(_dt.timezone.utc)
    )
    tiempo_esperado = _sql.Column(_sql.Integer, default=0)
    status = _sql.Column(_sql.Boolean, default=False)
    organizacion = _sql.Column(_sql.String)
    ip = _sql.Column(_sql.String)
    port = _sql.Column(_sql.Integer)

    def to_dict(self):
        return {
            "id_nodo": self.id_nodo,
            "fecha_creacion": self.fecha_creacion.isoformat()
            if self.fecha_creacion
            else None,
            "tiempo_esperado": self.tiempo_esperado,
            "status": self.status,
            "organizacion": self.organizacion,
            "ip": self.ip,
            "port": self.port,
        }
