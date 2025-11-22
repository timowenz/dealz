import uuid
from sqlmodel import Field, SQLModel
from datetime import datetime


from typing import List, Optional
from sqlmodel import Relationship


class PriceHistory(SQLModel, table=True):
    id: str | None = Field(primary_key=True, default_factory=uuid.uuid4)
    deal_id: str = Field(foreign_key="dealz.id")
    price_in_cents: int | None = Field(default=None)
    url: str | None = Field(default=None)
    merchant: str | None = Field(
        default=None,
        description="The merchant name for the deal. Example: 'Amazon'.",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    dealz: Optional["Dealz"] = Relationship(back_populates="price_history")


class Dealz(SQLModel, table=True):
    id: str | None = Field(primary_key=True, default_factory=uuid.uuid4)
    product_name: str = Field(default=None)
    lowest_price: int | None = Field(default=None)
    price_history: List["PriceHistory"] = Relationship(back_populates="dealz")
    currency: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now())
