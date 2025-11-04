from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import SessionListResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.get("", response_model=SessionListResponse)
async def list_all_sessions(db: AsyncSession = Depends(get_db)):
    """
    GET /session - List all sessions for the authenticated user.
    """
    # TODO: Implement authentication
    # TODO: Load user sessions
    # TODO: Format with deltaTimeInSecond and sort by it

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
