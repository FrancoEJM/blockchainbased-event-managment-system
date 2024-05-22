import datetime as _dt
import sqlalchemy.orm as _orm
from models import  event_user_models as eu_md
from services import user_services as user_sv

async def user_inscription(event_id: int, user_id: int, db: _orm.Session):
    user = await user_sv.get_user_by_id(user_id, db)
    
    existing_inscription = db.query(eu_md.EventoUsuario).filter_by(id_evento=event_id, id_usuario=user_id).first()
    
    if existing_inscription:
        # Si el registro existe y tiene una fecha de baja, actualizar fecha_baja a None
        existing_inscription.fecha_baja = None
        existing_inscription.fecha_inscripcion = _dt.datetime.now(_dt.timezone.utc)
    else:
        # Si el registro no existe, crear uno nuevo
        user_inscription_obj = eu_md.EventoUsuario(
            id_evento = event_id,
            id_usuario = user_id,
            correo_electronico = user.correo_electronico,
            fecha_inscripcion = _dt.datetime.now(_dt.timezone.utc),
            fecha_baja = None
        )
        db.add(user_inscription_obj)
    
    # Confirmar los cambios en la base de datos
    db.commit()
    
    # Refrescar el objeto de inscripción
    if existing_inscription:
        db.refresh(existing_inscription)
        return existing_inscription
    else:
        db.refresh(user_inscription_obj)
        return user_inscription_obj

async def user_unsubscribe(event_id:int, user_id:int, db: _orm.Session):
    user_event = db.query(eu_md.EventoUsuario).filter_by(id_evento=event_id, id_usuario=user_id).first()
    
    if user_event:
        user_event.fecha_inscripcion = None
        user_event.fecha_baja = _dt.datetime.now(_dt.timezone.utc)
        db.commit()
        db.refresh(user_event)
        return user_event

async def is_signed(event_id:int, user_id:int, db: _orm.Session):
    user_event = db.query(eu_md.EventoUsuario).filter_by(id_evento=event_id, id_usuario=user_id).first()
    if user_event:
        return True
    return False
