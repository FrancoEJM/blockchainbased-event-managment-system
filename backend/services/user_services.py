import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import datetime as _dt
from schemas import user_schemas as user_sch
from models import (
    user_models as user_md,
    event_user_models as event_user_md,
    event_models as event_md,
)
from services import (
    database_services as db_sv,
    util_services as util_sv,
    cryptography_services as crypto_sv,
)
import dotenv
import os
import jwt as _jwt

dotenv.load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
OAuth2Schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")


async def get_user_by_email(email: str, db: _orm.Session):
    return (
        db.query(user_md.Usuario)
        .filter(user_md.Usuario.correo_electronico == email)
        .first()
    )


async def get_user_by_id(id: int, db: _orm.Session):
    return db.query(user_md.Usuario).filter(user_md.Usuario.id_usuario == id).first()


async def create_user(user: user_sch.UserCreate, db: _orm.Session):
    user_obj = user_md.Usuario(
        correo_electronico=user.correo_electronico,
        hash_contrasena=_hash.bcrypt.hash(user.hash_contrasena),
        nombre=user.nombre,
        apellido=user.apellido,
        fecha_nacimiento=user.fecha_nacimiento,
        telefono=user.telefono,
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    await crypto_sv.create_cryptographic_credentials(user_obj.id_usuario, db)
    return user_obj


async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(email, db)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user


async def get_current_user(
    db: _orm.Session = _fastapi.Depends(db_sv.get_db),
    token: str = _fastapi.Depends(OAuth2Schema),
):
    try:
        payload = _jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user = db.query(user_md.Usuario).get(payload["id_usuario"])
    except Exception as e:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_401_UNAUTHORIZED,
            detail=f"Correo o contraseña incorrectos {e}",
        )

    return user_sch.User.model_validate(user)


async def save_attendee_data(
    event_id: int, gender: int, fullname: str, birthdate: _dt.date, db: _orm.Session
):
    birth_datetime = _dt.datetime.combine(birthdate, _dt.time.min)
    attendee_data_obj = event_user_md.EventoUsuario(
        id_usuario=0,
        id_evento=event_id,
        genero=gender,
        nombre_completo=fullname,
        fecha_nacimiento=birth_datetime,
    )
    db.add(attendee_data_obj)
    db.commit()
    db.refresh(attendee_data_obj)
    return attendee_data_obj


async def is_invited(event_id: int, email: str, token: str, db: _orm.Session):
    invitation = (
        db.query(event_md.EventosQRPrivados)
        .filter_by(
            correo_electronico=email,
            id_evento=event_id,
            token=token,
            token_utilizado=False,
        )
        .first()
    )
    if invitation:
        invitation.token_utilizado = True
        db.add(invitation)
        db.commit()
        db.refresh(invitation)

    return invitation


async def get_user_stats(user_id: int, db: _orm.Session):
    # Obtener todos los eventos creados por el usuario
    eventos = db.query(event_md.Eventos).filter_by(usuario_creador=user_id).all()

    # Lista para almacenar las estadísticas de los asistentes
    asistentes_stats = []

    for evento in eventos:
        # Obtener todos los registros de los asistentes a este evento
        asistentes = (
            db.query(event_user_md.EventoUsuario, event_md.EventosDefinicion.nombre)
            .join(
                event_md.EventosDefinicion,
                event_user_md.EventoUsuario.id_evento
                == event_md.EventosDefinicion.id_evento,
            )
            .filter(event_user_md.EventoUsuario.id_evento == evento.id_evento)
            .all()
        )

        for asistente, nombre_evento in asistentes:
            id_evento = asistente.id_evento
            genero = asistente.genero
            edad = util_sv.calculate_age(asistente.fecha_nacimiento)
            invitado = asistente.invitado

            asistentes_stats.append(
                {
                    "id_evento": id_evento,
                    "nombre_evento": nombre_evento,
                    "genero": genero,
                    "edad": edad,
                    "invitado": invitado,
                }
            )

    return asistentes_stats
