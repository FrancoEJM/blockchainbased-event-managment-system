import sqlalchemy.orm as _orm
import httpx
from models import user_models as user_md
import os

SMTP_URL = os.getenv("SMTP_URL")
IMG_SRC = '../data/userPrivateQRImages/image.png'


async def get_gender(db: _orm.Session):
    return db.query(user_md.Genero).filter(user_md.Genero.id_genero != 0).all()

async def send_invitation_email(receiver: str, event_name:str, url_redirect:str):
    url = f"{SMTP_URL}/enviar-correo/"

    correo_data = {
        "destinatario": receiver,
        "asunto": "Prueba",
        "cuerpo": f'<h1>Correo HTML {event_name}</h1><p>Este es un correo HTML de ejemplo. {url_redirect}</p><img src="{IMG_SRC}" alt="un qr" />',
        "es_html": True,
        "ruta_imagen": ""
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=correo_data)

        response.raise_for_status() 
        return response.json()

    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
    except httpx.RequestError as e:
        print(f"Request error occurred: {e}")
