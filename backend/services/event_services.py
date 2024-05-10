import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from schemas import user_schemas as user_sch, event_schemas as event_sch
from models import user_models as user_md, event_models as event_md, event_user_models as event_user_md
from services import database_services as db_sv

async def get_user_by_email(email:str, db: _orm.Session):
    return db.query(user_md.Usuario).filter(user_md.Usuario.correo_electronico == email).first()

async def get_categories(db: _orm.Session):
    return db.query(event_md.EventosCategoria).all()

async def get_modalities(db: _orm.Session):
    return db.query(event_md.EventosModalidad).all()

async def get_languages(db: _orm.Session):
    return db.query(event_md.EventosIdioma).all()

async def get_privacities(db: _orm.Session):
    return db.query(event_md.EventosPrivacidad).all()

async def create_event_record(event_author: int, db: _orm.Session):
    event_record_obj = event_md.Eventos(
        usuario_creador=event_author
    )
    db.add(event_record_obj)
    db.commit()
    db.refresh(event_record_obj)
    return event_record_obj.id_evento


async def create_event(id:int, event: event_sch.EventCreate, db: _orm.Session):
    event_obj = event_md.EventosDefinicion(
        id_evento = id,
        nombre = event.nombre,
        categoria = event.categoria,
        hora_inicio = event.hora_inicio,
        hora_fin = event.hora_fin,
        fecha = event.fecha,
        idioma = event.idioma,
        privacidad = event.privacidad,
        modalidad = event.modalidad,
        url_evento = event.url_evento,
        direccion = event.direccion,
        latitud = event.latitud,
        longitud = event.longitud
    )
    db.add(event_obj)
    db.commit()
    db.refresh(event_obj)
    return event_obj

async def save_event_image(id, name, path, db:_orm.Session):
    image_obj = event_md.EventosImagenes(
        id_evento = id,
        nombre = name,
        path = path
    )
    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)
    return image_obj;

async def save_event_guest(id, email, db:_orm.Session):
    existing_user = db.query(user_md.Usuario).filter(user_md.Usuario.correo_electronico == email).first()
    
    if existing_user:
        id_usuario = existing_user.id_usuario
    else:
        id_usuario = 0
    
    guest_obj = event_user_md.EventoInvitados(
        id_evento = id,
        id_usuario = id_usuario,
        correo_electronico = email,
    )
    db.add(guest_obj)
    db.commit()
    db.refresh(guest_obj)

    return id_usuario

    

