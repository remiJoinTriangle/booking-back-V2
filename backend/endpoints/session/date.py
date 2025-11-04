from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HttpPostSessionDateArguments, SessionWithHotelsResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/date", response_model=SessionWithHotelsResponse)
async def change_date_of_session(
    session_id: int,
    arguments: HttpPostSessionDateArguments,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session/{session_id}/date - Change date of a session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Update session date (packed_date format)
    # TODO: Return session.to_front() format with message, hotels, allVibes

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
