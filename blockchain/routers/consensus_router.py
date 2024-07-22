import fastapi as _fastapi
import asyncio

router = _fastapi.APIRouter()


@router.post("/poet-wait")
async def poet_wait(data: dict):
    assigned_time = data["assigned_time"]
    await asyncio.sleep(assigned_time)
    return {"status": "done", "assigned_time": assigned_time}
