import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

from schemas import user_schemas as user_sch, event_schemas as event_sch
from services import database_services as db_sv, user_services as user_sv, token_services as token_sv, event_services as event_sv
from models import event_models as event_md
router = _fastapi.APIRouter()

@router.get("/api/event/create")
async def get_select_data(db:_orm.Session = _fastapi.Depends(db_sv.get_db)):
    db_category = await event_sv.get_categories(db)
    db_modality = await event_sv.get_modalities(db)
    db_language = await event_sv.get_languages(db)
    db_privacity= await event_sv.get_privacities(db)

    data = {
        "categoria": db_category,
        "modalidad": db_modality,
        "idioma": db_language,
        "privacidad": db_privacity
    }
    return data

@router.post("/api/event/create")
async def create_new_event(event: event_sch.EventCreate,
                           db: _orm.Session= _fastapi.Depends(db_sv.get_db)):
    record_event = await event_sv.create_event_record(event.id_creador, db)
    print('-----------------------------------------------------------')
    print(record_event)
    print('-----------------------------------------------------------')
    return 0
    # return await event_sv.create_event(event,db)
    