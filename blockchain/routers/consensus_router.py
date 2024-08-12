import fastapi as _fastapi
import asyncio
import time
from services import node_services as node_sv

router = _fastapi.APIRouter()


# @router.post("/poet-wait")
# async def poet_wait(data: dict):
#     assigned_time = data["assigned_time"]
#     client_timestamp = data["timestamp"]
#     # Espera del nodo
#     await asyncio.sleep(assigned_time)
#     # Momento en el cual ha concluido la espera
#     server_timestamp = time.time()
#     return {
#         "status": _fastapi.status.HTTP_200_OK,
#         "assigned_time": assigned_time,
#         "client_timestamp": client_timestamp,
#         "server_timestamp": server_timestamp,
#     }


@router.post("/poet-wait")
async def poet_wait(data: dict):
    try:
        assigned_time = data["assigned_time"]
        client_timestamp = data["timestamp"]
    except KeyError as e:
        raise _fastapi.HTTPException(
            status_code=_fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"Missing required field: {str(e)}",
        )

    # Espera del nodo
    await asyncio.sleep(assigned_time)

    # Momento en el cual ha concluido la espera
    server_timestamp = time.time()

    return {
        "status": _fastapi.status.HTTP_200_OK,
        "assigned_time": assigned_time,
        "client_timestamp": client_timestamp,
        "server_timestamp": server_timestamp,
    }
