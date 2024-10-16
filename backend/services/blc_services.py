import sqlalchemy.orm as _orm
from models import event_models as event_md, event_user_models as event_user_md
from services import cryptography_services as crypto_sv
import httpx
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()
BLOCKCHAIN_URL = os.getenv("BLOCKCHAIN_URL")


async def collect_event_json(event_id: int, user_id: int, db: _orm.Session):
    # Obtener las llaves
    public_key, private_key = await crypto_sv.get_keys(user_id, db)
    # Recolectar transacciones
    transacciones = await collect_event_transactions(event_id, db)
    # Generar firma digital
    firma_digital = await crypto_sv.digital_signature(private_key, transacciones)

    # Crear diccionario inicial con los datos fijos
    json = {
        "id_evento": event_id,
        "organizador": user_id,
        "organizacion": "robleaustral",
        "llave_publica": public_key,
        "transacciones": transacciones,
        "firma_digital": firma_digital,
    }

    return json


async def collect_event_transactions(event_id: int, db: _orm.Session):
    transactions = []

    # Lógica para recolectar transacciones basadas en el event_id
    eventos_creacion = (
        db.query(event_md.Eventos)
        .filter(event_md.Eventos.id_evento == event_id)
        .first()
    )

    eventos_definicion = (
        db.query(event_md.EventosDefinicion)
        .filter(event_md.EventosDefinicion.id_evento == event_id)
        .first()
    )

    # Lógica para tipo 1: inicio del evento
    if eventos_creacion.fecha_ejecucion:
        transaction = {
            "tipo": 1,
            "detalle": {
                "fecha_inicio": eventos_creacion.fecha_ejecucion.isoformat(),
                "usuario": eventos_creacion.usuario_creador,
                "nombre_evento": eventos_definicion.nombre,
                "tipo_evento": eventos_definicion.privacidad,  # Ejemplo, ajusta según tu modelo
            },
        }
        transactions.append(transaction)

    # Lógica para tipo 2: ingreso de un usuario
    asistentes = (
        db.query(event_user_md.EventoUsuario)
        .filter(event_user_md.EventoUsuario.id_evento == event_id)
        .all()
    )

    for asistente in asistentes:
        transaction = {
            "tipo": 2,
            "detalle": {
                "fecha_ingreso": asistente.fecha_arribo.isoformat()
                if asistente.fecha_arribo
                else None,
                "usuario": asistente.id_usuario,
                "validado": 1 if asistente.invitado else 0,  # Ajusta según tu lógica
            },
        }
        transactions.append(transaction)

    # Lógica para tipo 3: fin del evento
    if eventos_creacion.fecha_finalizacion:
        transaction = {
            "tipo": 3,
            "detalle": {
                "fecha_cierre": eventos_creacion.fecha_finalizacion.isoformat(),
                "usuario": eventos_creacion.usuario_creador,
                "nombre_evento": eventos_definicion.nombre,
                "tipo_evento": eventos_definicion.privacidad,  # Ejemplo, ajusta según tu modelo
            },
        }
        transactions.append(transaction)

    return transactions


async def send_blc_data(event_id: int, user_id: int, db: _orm.Session):
    BLC_JSON = await collect_event_json(event_id, user_id, db)
    if not BLOCKCHAIN_URL:
        raise ValueError(
            "La URL de la blockchain no está configurada en el archivo .env."
        )

    URL = f"{BLOCKCHAIN_URL}/blockchain/process-transactions"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                URL,
                json=BLC_JSON,  # Enviar el JSON en el cuerpo de la solicitud
                headers={"Content-Type": "application/json"},
            )

            # Verificar la respuesta
            if response.status_code == 200:
                print(f"Transacciones del evento {event_id} procesadas correctamente.")
            else:
                print(
                    f"Error al procesar las transacciones del evento {event_id}: {response.status_code}"
                )
                print(
                    response.text
                )  # Cambiar response.json() por response.text para verificar el contenido de la respuesta
        except httpx.RequestError as e:
            print(f"Error en la solicitud HTTP: {str(e)}")
        except httpx.HTTPStatusError as e:
            print(f"Error de estado HTTP: {str(e)}")
        except httpx.HTTPStatusError as e:
            print(f"Error de estado HTTP: {str(e)}")
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            # Imprimir el contenido de la respuesta para ayudar en la depuración
            if "response" in locals():
                print(f"Contenido de la respuesta: {response.text}")
