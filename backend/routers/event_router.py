import fastapi as _fastapi
import fastapi.security as _security
import typing as _typing

import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

from schemas import user_schemas as user_sch, event_schemas as event_sch
from services import database_services as db_sv, user_services as user_sv, token_services as token_sv, event_services as event_sv
from models import event_models as event_md

import dotenv,os
import resend
import qrcode

router = _fastapi.APIRouter()

dotenv.load_dotenv()
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
UPLOAD_DIRECTORY = "/data/eventImages/"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

@router.get("/api/events")
async def get_events_list(id:int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    db_events = await event_sv.get_events(id,db)
    return db_events

@router.get("/api/user/events")
async def get_user_events(user_id: int,db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    db_user_events = await event_sv.get_user_events(user_id, db)
    return db_user_events

@router.get("/api/event")
async def get_event(id,db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    db_event = await event_sv.get_event(id,db)
    return db_event

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
    
@router.post("/api/event/upload")
async def upload_event_image(id: int, file: _fastapi.UploadFile = _fastapi.File(...), db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        new_filename = f"{id}_{file.filename}"
        with open(os.path.join(UPLOAD_DIRECTORY, new_filename), "wb") as buffer:
            buffer.write(await file.read())

        new_image = await event_sv.save_event_image(id, file.filename, f"{UPLOAD_DIRECTORY}{new_filename}",db)

        return {"new_image": new_image}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=str(e))
    
@router.post("/api/event/upload_default")
async def upload_event_image_default(id: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        new_filename = 'default.jpg'
        new_image = await event_sv.save_event_image_default(id,db)

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

@router.post("/api/event/mail")
async def send_emails_to_guest():
    resend.api_key = os.environ["RESEND_API_KEY"]

    params: resend.Emails.SendParams = {
        "sender": "Franco <guest@resend.dev>",
        "to": ['franco.mjimenez@gmail.com'],
        "subject": "hi",
        "html": "<strong>hello, world!</strong>",
    }

    try:
        email = resend.Emails.send(params)
        print(email)
    except Exception as e:
        print("Error al enviar el correo electrónico:", e)

    return(email)

@router.post("/api/event/start")
async def start_event(event_id: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        execution_date = await event_sv.start_event(event_id, db)
        event_features = await event_sv.get_event(event_id, db)
        if execution_date and event_features.privacidad == 1:
            qr_data = await create_public_qr_code(event_id,db)
            return execution_date, qr_data["qr_image_path"]
        elif execution_date and event_features.privacidad == 2:
            return {"es":"privado"} 
        else:
            raise _fastapi.HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=f"Failed to start event: {str(e)}")


@router.post("/api/event/end")
async def end_event(event_id: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        finished_event = await event_sv.end_event(event_id, db)
        if finished_event:
            return finished_event
        else:
            raise _fastapi.HTTPException(status_code=404, detail=f"Event with id {event_id} not found")
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=f"Failed to end event: {str(e)}")


@router.delete("/api/event")
async def delete_event(event_id: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    try:
        with db.begin():
            # Delete from BLC_EVENTOS_INVITADOS (multiple records)
            await event_sv.delete_event_invitados(event_id, db)
            # Delete from BLC_IMAGENES (single record)
            await event_sv.delete_event_imagen(event_id, db)
            # Delete from BLC_EVENTO_USUARIO (single record)
            await event_sv.delete_event_usuario(event_id, db)
            # Delete from BLC_EVENTOS (single record)
            await event_sv.delete_event(event_id, db)
            # Delete from BLC_EVENTOS_CREACION (single record)
            await event_sv.delete_event_creacion(event_id, db)
        return {"message": f"El evento {event_id} ha sido eliminado."}
    except Exception as e:
        raise _fastapi.HTTPException(status_code=500, detail=f"Failed to delete event: {str(e)}")

@router.post("/api/create-qr-code")
async def create_public_qr_code(event_id: int, db: _orm.Session = _fastapi.Depends(db_sv.get_db)):
    frontend_url = os.getenv("FRONTEND_URL")
    qr_url = f"{frontend_url}/data/{event_id}"

    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    qr_img_path = f"data/publicQRImages/event_{event_id}_qr.png"
    qr_img.save(qr_img_path)

    qr_db = await event_sv.save_qr_database(qr_img_path, event_id, db)

    if qr_db is None:
        raise _fastapi.HTTPException(status_code=500, detail="Error al guardar el código QR en la base de datos")

    return {"qr_image_path": qr_img_path, "qr_url": qr_url, "qr_db": qr_db.id_qr}


@router.get("/get-qr/{qr_image_path:path}")
async def get_qr(qr_image_path: str):
    # Devolver la imagen del QR
    return _fastapi.responses.FileResponse(qr_image_path)
