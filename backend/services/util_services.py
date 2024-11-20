import sqlalchemy.orm as _orm
import httpx
from models import user_models as user_md
import os
from services import event_services as event_sv
import typing as _typing
import datetime as _dt

SMTP_URL = os.getenv("SMTP_URL")
FRONTEND_URL = os.getenv("FRONTEND_URL")
IMG_SRC = "../data/userPrivateQRImages/image.png"


async def get_gender(db: _orm.Session):
    return db.query(user_md.Genero).filter(user_md.Genero.id_genero != 0).all()


async def send_invitation_email(
    event_id: str, guests: _typing.List[_typing.Dict[str, _typing.Any]], db
):
    smtp_responses = 0
    event = await event_sv.get_event(event_id, db)
    event_name = event.nombre
    url = f"{SMTP_URL}/enviar-correo/"

    for guest in guests:
        destinatario = guest["correo_electronico"]
        correo_data = {
            "destinatario": destinatario,
            "asunto": f"Invitación: {event_name}",
            "cuerpo": f"<h1>Felicidades, has sido invitado a {event_name}</h1><br><p>Por favor, guarda el siguiente código QR, el cual será solicitado en puerta para poder acceder al evento.</p>",
            "es_html": True,
            "ruta_imagen": f'../backend/data/userPrivateQRImages/{event_id}_{destinatario.split('@')[0]}.png',
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=correo_data)

            response.raise_for_status()
            smtp_responses += 1

        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")

    return smtp_responses


def calculate_age(birthdate):
    if birthdate:
        try:
            if isinstance(birthdate, _dt.datetime):
                birthdate = (
                    birthdate.date()
                )  # Convertir a datetime.date si es datetime.datetime
            elif isinstance(birthdate, _dt.date):
                pass
            else:
                return None

            today = _dt.date.today()
            age = (
                today.year
                - birthdate.year
                - ((today.month, today.day) < (birthdate.month, birthdate.day))
            )
            return age
        except ValueError:
            # Fecha de nacimiento inválida
            return None
    else:
        # Fecha de nacimiento es None o vacía
        return None
