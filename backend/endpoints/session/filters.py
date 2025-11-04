from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HttpPostSessionFiltersArguments, SessionWithHotelsResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/filters", response_model=SessionWithHotelsResponse)
async def change_filters_of_session(
    session_id: int,
    arguments: HttpPostSessionFiltersArguments,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session/{session_id}/filters - Change filters of a session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Convert filter booleans to flag and vibe_flag integers
    # TODO: Update session filters (flag, vibe_flag, price)
    # TODO: Return session.to_front() format with message, hotels, allVibes

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
