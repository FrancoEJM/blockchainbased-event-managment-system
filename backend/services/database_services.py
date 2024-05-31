import sys
import os

# Agregar el directorio al PYTHONPATH
database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(database_dir)

import database as _database


def create_db():
     return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


create_db()