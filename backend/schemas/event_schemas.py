import datetime as _dt

import pydantic as _pydantic


class _EventBase(_pydantic.BaseModel):
    id_creador: int


# class EventCreate(_EventBase):
#     nombre: str
#     categoria: int
#     hora_inicio: _dt.time
#     hora_fin: _dt.time
#     fecha: _dt.date
#     idioma: int
#     privacidad: int
#     modalidad: int
#     url_evento: str
#     direccion: str
#     latitud: float
#     longitud: float


class EventCreate(_EventBase):
    nombre: str
    categoria: int
    hora_inicio: _dt.time
    hora_fin: _dt.time
    fecha: _dt.date
    idioma: int
    privacidad: int
    direccion: str
    latitud: float
    longitud: float
    descripcion: str


class ImageUpload(_pydantic.BaseModel):
    id_evento: int
    nombre: str
    path: str
