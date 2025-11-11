from typing import Any

from pydantic import BaseModel
from sqlalchemy.inspection import inspect


class HotelFilter(BaseModel):
    city: str | None = None
    min_price: float | None = None
    max_price: float | None = None
    min_stars: int | None = None
    max_stars: int | None = None
