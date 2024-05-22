import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

from schemas import user_schemas as user_sch
from services import database_services as db_sv, user_services as user_sv, token_services as token_sv, event_user_services as eu_sv
from models import event_user_models as eu_md

router = _fastapi.APIRouter()

@router.post("/api/user/inscription")
async def user_inscription(event_id: int,user_id: int ,db:_orm.Session= _fastapi.Depends(db_sv.get_db)):
    user_inscription = await eu_sv.user_inscription(event_id,user_id,db)
    return user_inscription

@router.post("/api/user/unsubscribe")
async def user_unsubscribe(event_id: int,user_id: int ,db:_orm.Session= _fastapi.Depends(db_sv.get_db)):
    user_unsubscribe = await eu_sv.user_unsubscribe(event_id, user_id, db)
    return user_unsubscribe

@router.get("/api/user/is_signed")
async def is_signed(event_id: int,user_id: int ,db:_orm.Session= _fastapi.Depends(db_sv.get_db)):
    return await eu_sv.is_signed(event_id, user_id, db)   