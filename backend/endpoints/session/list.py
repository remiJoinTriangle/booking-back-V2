from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import SessionListResponse, SessionResponse
from ...services.session_service import get_sessions

router = APIRouter(prefix="/session", tags=["session"])


@router.get("", response_model=SessionListResponse)
async def list_all_sessions(db: AsyncSession = Depends(get_db)):
    """
    GET /session - List all sessions for the authenticated user.
    """
    # TODO: Implement authentication
    # TODO: Add `deltaTimeInSecond` to each session and sort sessions descendingly by it
    # TODO: Get sessions of current authenticated user instead of first 5 sessions
    sessions = await get_sessions(db, limit=5)

    # Format sessions
    formatted_sessions = [SessionResponse.from_orm(session) for session in sessions]

    return SessionListResponse(sessions=formatted_sessions)
