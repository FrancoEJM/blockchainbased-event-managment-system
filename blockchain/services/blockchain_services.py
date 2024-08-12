import fastapi as _fastapi
import sqlalchemy.orm as _orm
import sqlalchemy as _sqlalchemy
import datetime as _dt
import json as json_lib
from models import blockchain_models as blc_md
from services import (
    transaction_services as tx_sv,
    cryptography_services as crypto_sv,
    block_services as block_sv,
    sync_services as sync_sv,
    compression_services as compress_sv,
)
import os
import dotenv


async def get_active_nodes(db: _orm.Session):
    return db.query(blc_md.NODOS).filter(blc_md.NODOS.status).all()


async def update_node_status(ip: str, port: int, status: bool, db: _orm.Session):
    node = (
        db.query(blc_md.NODOS)
        .filter(blc_md.NODOS.ip == ip, blc_md.NODOS.port == port)
        .first()
    )
    if node:
        node.status = status
        db.commit()


async def get_next_block_number(db: _orm.Session):
    block_count = db.query(_sqlalchemy.func.count(blc_md.BLOQUES.id_bloque)).scalar()
    next_block_number = block_count + 1
    return f"{next_block_number:08d}"


async def add_new_block(event_data, waited_time: float, db: _orm.Session):
    """
    1. Validar firma digital ✅
    2. Validar transacciones
    3. Escribir bloque en formato
    4. Encriptar las transacciones
    5. Propagar el bloque por la red
    """
    response_message = {}
    # Validar firma digital
    digital_signature = await crypto_sv.check_digital_signature(event_data)
    if not digital_signature:
        return {
            "status": _fastapi.status.HTTP_401_UNAUTHORIZED,
            "message": "La firma digital no es válida",
            "steps": response_message,
        }
    response_message["firma_digital"] = "ok"

    # Validar transacciones
    valid_transactions = await tx_sv.validate_transactions(event_data)
    if not valid_transactions:
        return {
            "status": _fastapi.status.HTTP_400_BAD_REQUEST,
            "message": "Las transacciones no son válidas",
            "steps": response_message,
        }
    response_message["transacciones_validas"] = "ok"

    # Construcción del bloque
    writed = await block_sv.write_block(event_data, waited_time, db)
    if not writed:
        return {
            "status": _fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "No se ha podido registrar el bloque",
            "steps": response_message,
        }
    response_message["bloque_escrito"] = "ok"

    # Compresión
    zipped = await compress_sv.zip_block(writed["filename"])
    zipped = True
    if not zipped:
        return {
            "status": _fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            "message": "No se ha podido comprimir el bloque agregado",
            "steps": response_message,
        }
    response_message["bloque_comprimido"] = "ok"

    # Adición del bloque a la red
    shared = await sync_sv.spread_block(writed["filename"], db)
    if not shared:
        return {
            "status": _fastapi.status.HTTP_503_SERVICE_UNAVAILABLE,
            "message": "No se ha podido compartir el nuevo bloque a la red",
            "steps": response_message,
        }
    response_message["bloque_compartido"] = "ok"

    return {
        "status": 200,
        "message": response_message,
        "file_name": writed["filename"],
        "timestamp": writed["timestamp"],
        "node_id": os.getenv("NODE_ID"),
    }
