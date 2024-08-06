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
    max_block_number = db.query(_sqlalchemy.func.max(blc_md.BLOQUES.id_bloque)).scalar()
    next_block_number = max_block_number or 0
    return f"{next_block_number:08d}"


async def add_new_block(event_data, waited_time: float, db: _orm.Session):
    """
    1. Validar firma digital.
    2. Validar transacciones
    3. Escribir bloque en formato
    4. Encriptar las transacciones
    5. Propagar el bloque por la red
    """

    # Validar firma digital
    digital_signature = await crypto_sv.check_digital_signature(event_data)
    if not digital_signature:
        return {
            "status": _fastapi.status.HTTP_406_NOT_ACCEPTABLE,
            "message": "La firma digital no es válida",
        }

    # Validar transacciones
    valid_transactions = await tx_sv.validate_transactions(event_data)
    if not valid_transactions:
        return {
            "status": _fastapi.status.HTTP_406_NOT_ACCEPTABLE,
            "message": "Las transacciones no son válidas",
        }

    writed = await block_sv.write_block(event_data, waited_time, db)
    if not writed:
        return {
            "status": _fastapi.status.HTTP_406_NOT_ACCEPTABLE,
            "message": "No se ha podido registrar el bloque",
        }

    return {
        "status": 200,
        "message": "ok",
        "file_name": writed["filename"],
        "timestamp": writed["timestamp"],
        "node_id": os.getenv("NODE_ID"),
    }
