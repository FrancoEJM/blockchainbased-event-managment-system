import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from schemas import user_schemas as user_sch
from models import user_models as user_md, event_models as event_md
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