from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv

from routers.v1 import dealz_router
from database import get_db
from services.dealz_bot import DealzBot
from fastapi.middleware.cors import CORSMiddleware
import os

load_dotenv()

ORIGIN = os.getenv("ORIGIN")

origins = [ORIGIN]


@asynccontextmanager
async def lifespan(app: FastAPI):
    dealz_bot = DealzBot(db=next(get_db()))
    results: dict = await dealz_bot.search_prices(product_name="Sony WH-1000XM5")
    print(results)
    yield


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=dealz_router.router, prefix="/api/v1")
