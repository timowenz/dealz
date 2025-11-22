from sqlmodel import Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv("DB_DRIVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

assert all([DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]), (
    "Database configuration values must not be None"
)


connection_url = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
db_engine = create_engine(connection_url)


def get_db():
    """FastAPI dependency for database sessions"""
    with Session(db_engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
