from sqlmodel import Field, SQLModel
from datetime import datetime


class Dealz(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    product_name: str = Field(default=None)
    price: int | None = Field(default=None)
    currency: str | None = Field(default=None)
    url: str | None = Field(default=None)
    merchant: str | None = Field(default=None)
    created_at: datetime | None = Field(default_factory=lambda: datetime.now())
    updated_at: datetime | None = Field(default_factory=lambda: datetime.now())
