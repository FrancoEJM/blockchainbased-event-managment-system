import datetime as _dt

import pydantic as _pydantic


class _UserBase(_pydantic.BaseModel):
    correo_electronico: str


class UserCreate(_UserBase):
    hash_contrasena: str
    nombre: str
    apellido: str
    fecha_nacimiento: _dt.date
    telefono: int

    class Config:
        from_attributes = True


class User(_UserBase):
    id_usuario: int

    class Config:
        from_attributes = True


class UserDetails(_UserBase):
    id_usuario: int
    nombre: str
    apellido: str
    correo_electronico: str


class AttendeeDetails(_pydantic.BaseModel):
    event_id: int
    gender: int
    fullname: str
    birthdate: _dt.date

    class Config:
        from_attributes = True
