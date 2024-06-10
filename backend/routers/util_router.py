import fastapi as _fastapi
import sqlalchemy.orm as _orm
import os
import signal
from services import database_services as db_sv, util_services as ut_sv
router = _fastapi.APIRouter()

@router.get("/api/gender")
async def get_gender(db:_orm.Session = _fastapi.Depends(db_sv.get_db)):
    db_gender= await ut_sv.get_gender(db)
    return db_gender


@router.get("/shutdown")
async def shutdown_server():
    try:
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=str(e))
    return {"message": "Server is shutting down..."}