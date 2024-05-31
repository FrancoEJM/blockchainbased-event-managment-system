import sqlalchemy.orm as _orm
from models import user_models as user_md

async def get_gender(db: _orm.Session):
    return db.query(user_md.Genero).filter(user_md.Genero.id_genero != 0).all()