import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

DB_URL = DATABASE_URL

engine = _sql.create_engine(DB_URL, echo=True)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
