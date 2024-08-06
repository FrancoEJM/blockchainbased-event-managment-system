import fastapi as _fastapi
import sqlalchemy.orm as _orm
from services import (
    database_services as db_sv,
    blockchain_services as blc_sv,
    consensus_services as consensus_sv,
    util_services as util_sv,
    transaction_services as tx_sv,
    block_services as block_sv,
)
from models import blockchain_models as blc_md
from typing import List, Dict
import asyncio
import httpx
import json as json_lib

router = _fastapi.APIRouter()


# @router.post("/blockchain/process-transactions")
# async def process_transactions(
#     event_data: str, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
# ):
#     active_nodes = await blc_sv.get_active_nodes(db)
#     formatted_nodes = util_sv.convert_nodes(active_nodes)
#     selected_node = await consensus_sv.proof_of_elapsed_time(formatted_nodes, 8)
#     new_block = await blc_sv.add_new_block(
#         event_data, selected_node["real_waited_time"], db
#     )
#     return selected_node


@router.post("/blockchain/process-transactions")
async def process_transactions(
    request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    # Obtiene los datos del evento
    event_data = await request.json()

    # Obtiene los nodos activos de la red
    active_nodes = await blc_sv.get_active_nodes(db)
    formatted_nodes = util_sv.convert_nodes(active_nodes)

    # Aplica el mecanismo de consenso
    selected_node = await consensus_sv.proof_of_elapsed_time(formatted_nodes, 8)

    # Petición de adición de bloque al nodo escogido
    node_ip = selected_node["ip"]
    url = f"http://{node_ip}/blockchain/block"
    payload = {
        "event_data": event_data,
        "waited_time": selected_node["real_waited_time"],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)

    return response.json()
    # new_block = await blc_sv.add_new_block(
    #     event_data, selected_node["ip"], selected_node["real_waited_time"], db
    # )
    # return new_block


@router.post("/create-genesis-block")
async def create_genesis_block(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    genesis_event_data = json_lib.dumps(
        {
            "id_evento": "0",
            "transacciones": [],
            "llave_publica": "",
            "firma_digital": "",
            "organizador": "0",
            "organizacion": "robleaustral",
        }
    )

    genesis_block = await block_sv.write_block(genesis_event_data, 0, db)
    return {"message": "Genesis block created successfully", "block": genesis_block}


@router.get("/api/nodes")
async def get_events_list(db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    return await blc_sv.get_active_nodes(db)
