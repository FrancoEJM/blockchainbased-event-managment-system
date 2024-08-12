import fastapi as _fastapi
from services import (
    blockchain_services as blc_sv,
    database_services as db_sv,
    block_services as block_sv,
    node_services as node_sv,
)
import sqlalchemy.orm as _orm
import os
import shutil
import json
import datetime
from models import blockchain_models as blc_md

router = _fastapi.APIRouter()
BLOCKCHAIN_DIR = "/BLOCKCHAIN"


@router.post("/blockchain/block")
async def add_new_block(
    request: _fastapi.Request, db: _orm.Session = _fastapi.Depends(db_sv.get_db)
):
    data = await request.json()
    event_data = data.get("event_data")
    waited_time = data.get("waited_time")
    response = await blc_sv.add_new_block(event_data, waited_time, db)
    if response["status"] != 200:
        return {"status": response["status"], "message": response["message"]}

    await block_sv.record_block_data(
        event_data, response["file_name"], response["timestamp"], db
    )
    # await node_sv.record_node_data(response["node_id"], waited_time, db)

    return {"status": response["status"], "message": response["message"]}


@router.post("/blockchain/block/latest")
async def receive_block(
    file: _fastapi.UploadFile = _fastapi.File(...),
    db: _orm.Session = _fastapi.Depends(db_sv.get_db),
):
    try:
        # Guardar el archivo recibido en /BLOCKCHAIN/
        file_location = os.path.join(BLOCKCHAIN_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Leer y procesar el archivo del bloque
        with open(file_location, "r") as f:
            block_data = json.load(f)

        # Extraer datos del bloque
        block_number = block_data.get("block_number")
        timestamp = datetime.fromtimestamp(block_data.get("timestamp")).strftime(
            "%Y-%m-%d"
        )
        event_id = block_data.get("event_id")
        organization = block_data.get("organization")
        creator = block_data.get("organizer")

        # Crear un nuevo registro de bloque
        new_block = blc_md.BLOQUES(
            id_bloque=block_number,
            path=file_location,
            id_evento=event_id,
            org=organization,
            fecha_inicio=None,
            fecha_fin=None,
            creador=creator,
            timestamp=timestamp,
        )
        db.add(new_block)
        db.commit()

        return {
            "status": "success",
            "message": "Block received and processed successfully",
        }
    except Exception as e:
        print(f"Error receiving block: {str(e)}")
        db.rollback()
        raise _fastapi.HTTPException(
            status_code=500, detail=f"Error receiving block: {str(e)}"
        )


# @router.post("/create-first-block")
# async def create_first_block(request: _fastapi.Request):
#     # Verificar si ya existe algún archivo en /BLOCKCHAIN
#     existing_files = glob.glob(os.path.join(BLOCKCHAIN_DIR, "*.txt"))
#     if existing_files:
#         raise _fastapi.HTTPException(
#             status_code=400, detail="Ya existe un bloque en la blockchain"
#         )

#     # Leer el cuerpo de la solicitud
#     event_data = await request.json()

#     # Escribir el bloque
#     result = await write_block(json_lib.dumps(event_data))

#     return result
