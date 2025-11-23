from fastapi import APIRouter, Depends
from sqlalchemy.exc import OperationalError
from sqlmodel import Session

from database import get_db
from services.dealz_bot import DealzBot

router = APIRouter()


@router.get("/browser/{product_name}")
async def browser(product_name: str, db: Session = Depends(get_db)):
    try:
        dealz_bot = DealzBot(db=db)
        results: dict = await dealz_bot.search_prices(product_name=product_name)
        print(results)
        return {"productName": product_name, "results": results}
    except OperationalError as e:
        print(e)
        return {
            "error": "Database could not operate. Are you sure the database is ready for connection?"
        }
    except Exception as e:
        print(e)
        return {"error": str(e)}
