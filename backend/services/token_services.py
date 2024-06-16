import fastapi.security as _security
import jwt as _jwt
import dotenv
import os
import secrets
import sqlalchemy.orm as _orm
from models import user_models as user_md, event_models as event_md
from schemas import user_schemas as user_sch

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
OAuth2Schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")


async def create_token(user: user_md.Usuario):
    user_obj = user_sch.User.model_validate(user)
    token = _jwt.encode(user_obj.model_dump(), SECRET_KEY)

    return dict(access_token=token, token_type="bearer")


async def generate_unique_token(db: _orm.Session, length=16):
    while True:
        token = secrets.token_hex(length // 2)
        if not db.query(event_md.EventosQRPrivados).filter_by(token=token).first():
            return token
