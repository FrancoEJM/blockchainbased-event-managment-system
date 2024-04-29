import fastapi as _fastapi
import fastapi.security as _security

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

from schemas import user_schemas as user_sch
from services import database_services as db_sv, user_services as user_sv, token_services as token_sv, event_services as event_sv

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
