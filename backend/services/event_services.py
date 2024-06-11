import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import sqlalchemy as _sqlalchemy
import passlib.hash as _hash
import datetime as _dt
import typing as _typing
from schemas import user_schemas as user_sch, event_schemas as event_sch
from models import user_models as user_md, event_models as event_md, event_user_models as event_user_md
from services import database_services as db_sv


async def get_user_by_email(email:str, db: _orm.Session):
    return db.query(user_md.Usuario).filter(user_md.Usuario.correo_electronico == email).first()


async def get_categories(db: _orm.Session):
    return db.query(event_md.EventosCategoria).all()


async def get_modalities(db: _orm.Session):
    return db.query(event_md.EventosModalidad).all()


async def get_languages(db: _orm.Session):
    return db.query(event_md.EventosIdioma).all()


async def get_privacities(db: _orm.Session):
    return db.query(event_md.EventosPrivacidad).all()


async def create_event_record(event_author: int, db: _orm.Session):
    event_record_obj = event_md.Eventos(
        usuario_creador=event_author
    )
    db.add(event_record_obj)
    db.commit()
    db.refresh(event_record_obj)
    return event_record_obj.id_evento


async def create_event(id:int, event: event_sch.EventCreate, db: _orm.Session):
    event_obj = event_md.EventosDefinicion(
        id_evento = id,
        nombre = event.nombre,
        categoria = event.categoria,
        hora_inicio = event.hora_inicio,
        hora_fin = event.hora_fin,
        fecha = event.fecha,
        idioma = event.idioma,
        privacidad = event.privacidad,
        modalidad = event.modalidad,
        url_evento = event.url_evento,
        direccion = event.direccion,
        latitud = event.latitud,
        longitud = event.longitud
    )
    db.add(event_obj)
    db.commit()
    db.refresh(event_obj)
    return event_obj


async def start_event(event_id: int, db: _orm.Session):
    try:
        event_obj = db.query(event_md.Eventos).filter_by(id_evento=event_id).first()
        print(event_obj);
        if event_obj:
            event_obj.fecha_ejecucion = _dt.datetime.now(_dt.timezone.utc)
            db.commit()
            db.refresh(event_obj)
            return event_obj.fecha_ejecucion
        else:
            return None  # Evento no encontrado, manejar esto en el endpoint
    except Exception as e:
        raise e  # Propaga la excepción


async def end_event(event_id: int, db: _orm.Session):
    try:
        event_obj = db.query(event_md.Eventos).filter_by(id_evento=event_id).first()
        if event_obj:
            event_obj.fecha_finalizacion = _dt.datetime.now(_dt.timezone.utc)
            db.commit()
            db.refresh(event_obj)
            return event_obj
        else:
            return None
    except Exception as e:
        raise e  # Propaga la excepción


async def save_event_image(id, name, path, db:_orm.Session):
    image_obj = event_md.EventosImagenes(
        id_evento = id,
        nombre = name,
        path = path
    )
    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)
    return image_obj


async def save_event_image_default(id, db:_orm.Session):
    image_obj = event_md.EventosImagenes(
        id_evento = id,
        nombre = 'default.jpg',
        path = '/data/eventImages/default.jpg'
    )
    db.add(image_obj)
    db.commit()
    db.refresh(image_obj)
    return image_obj


async def save_event_guest(id: int, name:str, email:str, gender, birthdate, db:_orm.Session):
    existing_user = db.query(user_md.Usuario).filter(user_md.Usuario.correo_electronico == email).first()
    
    if existing_user:
        id_usuario = existing_user.id_usuario
    else:
        id_usuario = 0

    guest_obj = event_user_md.EventoInvitados(
        id_evento = id,
        id_usuario = id_usuario,
        correo_electronico = email,
        nombre = name,
        genero = gender,
        fecha_nacimiento = birthdate
    )
    
    db.add(guest_obj)
    db.commit()
    db.refresh(guest_obj)
    return guest_obj


async def get_events(user_id: int, db: _orm.Session):
    # Subconsulta para obtener los IDs de eventos privados a los que el usuario está invitado
    invited_events_subquery = db.query(event_user_md.EventoInvitados.id_evento).filter(event_user_md.EventoInvitados.id_usuario == user_id).subquery()

    # Consulta principal para obtener eventos públicos y privados donde el usuario está invitado
    events_query = db.query(event_md.EventosDefinicion).\
        options(
            _orm.joinedload(event_md.EventosDefinicion.categorias),
            _orm.joinedload(event_md.EventosDefinicion.idiomas),
            _orm.joinedload(event_md.EventosDefinicion.privacidades),
            _orm.joinedload(event_md.EventosDefinicion.modalidades),
            _orm.joinedload(event_md.EventosDefinicion.imagenes)
        ).filter(
            (event_md.EventosDefinicion.privacidad == 1) | 
            (event_md.EventosDefinicion.id_evento.in_(invited_events_subquery))
        )

    return events_query.all()


# async def get_user_events(user_id: int, db: _orm.Session):
#     events = (
#         db.query(event_md.EventosDefinicion)
#         .join(event_md.Eventos)
#         .filter(event_md.Eventos.usuario_creador == user_id)
#         .options(
#             _orm.joinedload(event_md.EventosDefinicion.categorias),
#             _orm.joinedload(event_md.EventosDefinicion.idiomas),
#             _orm.joinedload(event_md.EventosDefinicion.privacidades),
#             _orm.joinedload(event_md.EventosDefinicion.modalidades),
#             _orm.joinedload(event_md.EventosDefinicion.imagenes)
#         )
#         .all()
#     )
#     return events

async def get_user_events(user_id: int, db: _orm.Session) -> _typing.List[dict]:
    events = (
        db.query(event_md.EventosDefinicion, event_md.Eventos.fecha_ejecucion, event_md.Eventos.fecha_finalizacion)
        .join(event_md.Eventos)
        .filter(event_md.Eventos.usuario_creador == user_id)
        .options(
            _orm.joinedload(event_md.EventosDefinicion.categorias),
            _orm.joinedload(event_md.EventosDefinicion.idiomas),
            _orm.joinedload(event_md.EventosDefinicion.privacidades),
            _orm.joinedload(event_md.EventosDefinicion.modalidades),
            _orm.joinedload(event_md.EventosDefinicion.imagenes),
            _orm.joinedload(event_md.EventosDefinicion.qrs_publicos)
        )
        .all()
    )

    formatted_events = []
    for event_def, fecha_ejecucion, fecha_finalizacion in events:
        event_dict = event_def.__dict__
        event_dict['fecha_ejecucion'] = str(fecha_ejecucion) if fecha_ejecucion else None
        event_dict['fecha_finalizacion'] = str(fecha_finalizacion) if fecha_finalizacion else None
        formatted_events.append(event_dict)

    return formatted_events



async def get_event(id,db: _orm.Session):
    return db.query(event_md.EventosDefinicion).\
        options(
            _orm.joinedload(event_md.EventosDefinicion.categorias),
            _orm.joinedload(event_md.EventosDefinicion.idiomas),
            _orm.joinedload(event_md.EventosDefinicion.privacidades),
            _orm.joinedload(event_md.EventosDefinicion.modalidades),
            _orm.joinedload(event_md.EventosDefinicion.imagenes),
            _orm.joinedload(event_md.EventosDefinicion.qrs_publicos)
        ).filter(event_md.EventosDefinicion.id_evento == id).first()


async def delete_event_invitados(event_id: int, db: _orm.Session):
    db.query(event_user_md.EventoInvitados).filter(event_user_md.EventoInvitados.id_evento == event_id).delete()


async def delete_event_imagen(event_id: int, db: _orm.Session):
    db.query(event_md.EventosImagenes).filter(event_md.EventosImagenes.id_evento == event_id).delete()


async def delete_event_usuario(event_id: int, db: _orm.Session):
    db.query(event_user_md.EventoUsuario).filter(event_user_md.EventoUsuario.id_evento == event_id).delete()


async def delete_event(event_id: int, db: _orm.Session):
    db.query(event_md.EventosDefinicion).filter(event_md.EventosDefinicion.id_evento == event_id).delete()


async def delete_event_creacion(event_id: int, db: _orm.Session):
    db.query(event_md.Eventos).filter(event_md.Eventos.id_evento == event_id).delete()


async def save_qr_database(path: str, event_id: int, db: _orm.Session):
    qr_object = event_md.EventosQRPublicos(
        id_qr = event_id,
        id_evento = event_id,
        path = path
    )
    db.add(qr_object)
    try:
        db.commit()
        db.refresh(qr_object)
        return qr_object
    except Exception as e:
        db.rollback()
        print(f"Error al guardar QR en la base de datos: {str(e)}")
        raise _fastapi.HTTPException(status_code=404, detail="El evento especificado no existe para guardar el QR")



def get_event_stats(event_id: int, db: _orm.Session):
    numero_registros = db.query(_sqlalchemy.func.count(event_user_md.EventoUsuario.id_entrada)).filter(event_user_md.EventoUsuario.id_evento == event_id).scalar()

    detalles = db.query(
        user_md.Genero.id_genero,
        user_md.Genero.descripcion.label('genero'),
        event_user_md.EventoUsuario.fecha_nacimiento,
        event_user_md.EventoUsuario.invitado
    ).join(
        user_md.Genero, event_user_md.EventoUsuario.genero == user_md.Genero.id_genero
    ).filter(
        event_user_md.EventoUsuario.id_evento == event_id
    ).all()

    resultados = {
        'numero_registros': numero_registros,
        'detalles': [
            {
                'id_genero': detalle.id_genero,
                'genero': detalle.genero,
                'fecha_nacimiento': detalle.fecha_nacimiento,
                'invitado': detalle.invitado
            }
            for detalle in detalles
        ]
    }

    return resultados


async def parse_guests_data(event_id: int, guests: _typing.List[_typing.Dict[str, _typing.Any]], db):
    db_responses = []
    for guest_data in guests:
        name = guest_data['nombre']
        email = guest_data['correo_electronico']
        gender = guest_data['genero']
        birthdate = guest_data['fecha_nacimiento']
        gender_mapping = {
            'M': 1,
            'F': 2,
            'O': 3,
            'D': 0
        }

        if gender in gender_mapping:
            gender = gender_mapping[gender]

        try:
            guest_obj = await save_event_guest(event_id, name, email, gender, birthdate, db)
            db_responses.append({
                "correo_electronico": guest_obj.correo_electronico,
                "fecha_invitacion": guest_obj.fecha_invitacion,
                "nombre": guest_obj.nombre,
                "genero": guest_obj.genero,
            })
        except Exception as e:
            print(f"Error saving guest {name}: {str(e)}")
    return db_responses