import fastapi as _fastapi
import fastapi.security as _security
import typing as _typing

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

from schemas import user_schemas as user_sch, event_schemas as event_sch
from services import database_services as db_sv, user_services as user_sv, token_services as token_sv, event_services as event_sv
from models import event_models as event_md

import os

router = _fastapi.APIRouter()

UPLOAD_DIRECTORY = "./data/eventImages/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

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
    id = await event_sv.create_event_record(event.id_creador, db)
    create_event = await event_sv.create_event(id,event,db)
    return create_event
    
@router.post("/api/event/upload/")
async def upload_event_image(id: int, file: _fastapi.UploadFile = _fastapi.File(...), db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        new_filename = f"{id}_{file.filename}"
        with open(os.path.join(UPLOAD_DIRECTORY, new_filename), "wb") as buffer:
            buffer.write(await file.read())

        new_image = await event_sv.save_event_image(id, file.filename, f"{UPLOAD_DIRECTORY}{new_filename}",db)

        return {"new_image": new_image}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/event/guests")
async def upload_guests_list(event_id: int,q: _typing.List[str] = _fastapi.Query(None), db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    responses = []

    for i in range(len(q)):
        id_usuario = await event_sv.save_event_guest(event_id, q[i], db)
        responses.append({"email": q[i], "id_usuario": id_usuario})

    return {"responses": responses}
