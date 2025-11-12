from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class RoutingRoute(str, Enum):
    NEED_TO_EXTERNAL_SEARCH = "NEED_TO_EXTERNAL_SEARCH"
    NEED_TO_QUERY_FROM_DATABASE = "NEED_TO_QUERY_FROM_DATABASE"


class RoutingResponse(BaseModel):
    route: RoutingRoute = Field(
        ..., description="The route to take based on the user's request"
    )


class HotelFilter(BaseModel):
    min_price: float | None = Field(
        ..., description="The minimum price to filter the hotels by"
    )
    max_price: float | None = Field(
        ..., description="The maximum price to filter the hotels by"
    )
    min_stars: int | None = Field(
        ..., description="The minimum star rating to filter the hotels by"
    )
    max_stars: int | None = Field(
        ..., description="The maximum star rating to filter the hotels by"
    )
    cities: List[List[float]] | None = Field(
        ...,
        description="""
        Only give geopoints for explicitly mentioned cities in the user's request. format [latitude, longitude]
        """,
        min_length=1,
        max_length=10,
    )


class HotelFilterResponse(BaseModel):
    filter: HotelFilter = Field(..., description="The filter to apply to the hotels")


class RankingResponse(BaseModel):
    desc_sorted_hotels_ids: List[int] = Field(
        ...,
        description="The list of hotel ids sorted by relevance to the user's request",
    )
