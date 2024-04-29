import fastapi.security as _security
import jwt as _jwt
import dotenv
import os

from models import user_models as user_md
from schemas import user_schemas as user_sch

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
OAuth2Schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

async def create_token(user: user_md.Usuario):
    user_obj = user_sch.User.model_validate(user)
    token = _jwt.encode(user_obj.model_dump(), SECRET_KEY)

    return dict(access_token=token, token_type="bearer")