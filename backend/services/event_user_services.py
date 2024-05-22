import sqlalchemy.orm as _orm
from models import  event_user_models as eu_md
from services import user_services as user_sv

async def user_inscription(event_id:int, user_id:int, db: _orm.Session):
    user = await user_sv.get_user_by_id(user_id,db)
    print(user,"...............................................................................................................")
    user_inscription_obj = eu_md.EventoUsuario(
        id_evento = event_id,
        id_usuario = user_id,
        correo_electronico = user.correo_electronico
    )
    db.add(user_inscription_obj)
    db.commit()
    db.refresh(user_inscription_obj)
    return user_inscription_obj.id_evento