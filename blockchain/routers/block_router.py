import fastapi as _fastapi
from services import (
    blockchain_services as blc_sv,
    database_services as db_sv,
    block_services as block_sv,
    node_services as node_sv,
)
import sqlalchemy.orm as _orm

router = _fastapi.APIRouter()


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
    print(response)
    print(waited_time)
    await node_sv.record_node_data(response["node_id"], waited_time, db)

    return {"status": response["status"], "message": "Block added successfully"}


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
