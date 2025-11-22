from fastapi import APIRouter, Depends
from sqlalchemy.exc import OperationalError
from sqlmodel import Session

from database import get_db
from services.dealz_bot import DealzBot

router = APIRouter()


@router.get("/browser")
async def browser(db: Session = Depends(get_db)):
    try:
        dealz_bot = DealzBot(db=db)
        results: dict = await dealz_bot.search_prices(product_name="Sony WH-1000XM4")
        print(results)
        return results
    except OperationalError as e:
        print(e)
        return {
            "error": "Database could not operate. Are you sure the database is ready for connection?"
        }
    except Exception as e:
        print(e)
        return {"error": e}
