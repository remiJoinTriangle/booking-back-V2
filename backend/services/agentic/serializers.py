from enum import Enum

from pydantic import BaseModel, Field


class RoutingRoute(str, Enum):
    NEED_TO_PERFORM_SEARCH = "NEED_TO_PERFORM_SEARCH"
    NEED_TO_QUERY_FROM_DATABASE = "NEED_TO_QUERY_FROM_DATABASE"


class RoutingResponse(BaseModel):
    route: RoutingRoute = Field(
        ..., description="The route to take based on the user's request"
    )
