import database as _database
import sqlalchemy.ext.asyncio as _asyncio
from models import blockchain_models as blc_md
import logging


def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
