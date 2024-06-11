import sqlalchemy as _sql
import sqlalchemy.orm as _orm

DB_URL = "postgresql://fjm:123@localhost:5432/db_project"

engine = _sql.create_engine(DB_URL, echo=True)

SessionLocal = _orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
