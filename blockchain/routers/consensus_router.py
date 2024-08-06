import fastapi as _fastapi
import asyncio
import time

router = _fastapi.APIRouter()


@router.post("/poet-wait")
async def poet_wait(data: dict):
    assigned_time = data["assigned_time"]
    client_timestamp = data["timestamp"]
    # Espera del nodo
    await asyncio.sleep(assigned_time)
    # Momento en el cual ha concluido la espera
    server_timestamp = time.time()
    return {
        "status": "done",
        "assigned_time": assigned_time,
        "client_timestamp": client_timestamp,
        "server_timestamp": server_timestamp,
    }
