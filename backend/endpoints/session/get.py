from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import SessionWithHotelsResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/{session_id}", response_model=SessionWithHotelsResponse)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """
    GET /session/{session_id} - Get a specific session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Load session with last message
    # TODO: Format hotels with thumbnails, flags, vibes
    # TODO: Return session.to_front() format with message, hotels, allVibes

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
