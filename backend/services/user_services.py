import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from schemas import user_schemas as user_sch
from models import user_models as user_md
from services import database_services as db_sv
import dotenv, os
import jwt as _jwt

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
OAuth2Schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

async def get_user_by_email(email:str, db: _orm.Session):
    return db.query(user_md.Usuario).filter(user_md.Usuario.correo_electronico == email).first()

async def get_user_by_id(id:int, db: _orm.Session):
    return db.query(user_md.Usuario).filter(user_md.Usuario.id_usuario == id).first()


async def create_user(user: user_sch.UserCreate, db: _orm.Session):
    user_obj = user_md.Usuario(
        correo_electronico = user.correo_electronico,
        hash_contrasena = _hash.bcrypt.hash(user.hash_contrasena),
        nombre = user.nombre,
        apellido = user.apellido,
        fecha_nacimiento = user.fecha_nacimiento 
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email, db)

    if not user:
        return False

    if not user.verify_password(password):
        return False
    
    return user


async def get_current_user(db: _orm.Session = _fastapi.Depends(db_sv.get_db), token: str = _fastapi.Depends(OAuth2Schema)):
    try:
        payload = _jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = db.query(user_md.Usuario).get(payload["id_usuario"])
    except:
        raise _fastapi.HTTPException(status_code=_fastapi.status.HTTP_401_UNAUTHORIZED, detail="Correo o contraseña incorrectos")
    
    return user_sch.User.model_validate(user)