import fastapi as _fastapi
import sqlalchemy.orm as _orm
import sqlalchemy as _sqlalchemy
import datetime as _dt
from models import blc_models as blc_md


async def get_active_nodes(db: _orm.Session):
    return db.query(blc_md.NODOS).filter(blc_md.NODOS.status).all()
