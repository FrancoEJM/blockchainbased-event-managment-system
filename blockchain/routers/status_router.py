import fastapi as _fastapi

router = _fastapi.APIRouter()


@router.get("/ping")
async def get_node_status():
    return True
