import sqlalchemy.orm as _orm
import httpx
from models import user_models as user_md
import os
from services import event_services as event_sv
import typing as _typing

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
        correo_data = {
            "destinatario": guest["correo_electronico"],
            "asunto": "Prueba",
            "cuerpo": f'<h1>Correo HTML {event_name}</h1><p>Este es un correo HTML de ejemplo. {url}</p><img src="{IMG_SRC}" alt="un qr" />',
            "es_html": True,
            "ruta_imagen": "",
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
