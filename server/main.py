from fastapi import FastAPI
from sqlmodel import Session, create_engine, SQLModel
import os
from dotenv import load_dotenv

from models import Dealz


load_dotenv()

app = FastAPI()

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

try:
    SQLModel.metadata.create_all(db_engine)

    with Session(db_engine) as session:
        entry1 = Dealz(id=1, product_name="Sony WH-1000XM6", price=320)

        session.add(entry1)
        session.commit()


except Exception as e:
    print(e)
