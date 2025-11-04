from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HotelResponse, SessionResponse, SessionWithHotelsResponse
from ...services.session_service import (
    get_session_by_id,
    get_hotels_for_session,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/{session_id}", response_model=SessionWithHotelsResponse)
async def get_session(session_id: int, db: AsyncSession = Depends(get_db)):
    """
    GET /session/{session_id} - Get a specific session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership

    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Get all hotels
    hotels = await get_hotels_for_session(db, session)

    # Format hotels
    formatted_hotels = [HotelResponse.from_orm(hotel) for hotel in hotels]

    # Format session response
    session_response = SessionResponse.from_orm(session)

    # TODO: Format hotels with thumbnails, flags, vibes properly

    return SessionWithHotelsResponse(
        **session_response.model_dump(),
        message=None,  # TODO: Get and return the last message
        hotels=formatted_hotels,
        all_vibes=[],  # TODO: Build and return all vibes list
    )
