from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import UpdateSessionFiltersParameters, SessionWithHotelsResponse, SessionResponse, HotelResponse
from ...services.session_service import (
    get_session_by_id,
    update_session_filters,
    get_last_message_for_session,
    get_hotels_for_session,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/filters", response_model=SessionWithHotelsResponse)
async def change_filters_of_session(
    session_id: int,
    arguments: UpdateSessionFiltersParameters,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session/{session_id}/filters - Change filters of a session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Convert filter booleans to flag and vibe_flag integers

    # Get session
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session [{session_id}] does not exist")

    # Convert filters to dict
    filters_dict = arguments.model_dump()

    # Update session filters
    session = await update_session_filters(
        db=db,
        session=session,
        filters=filters_dict,
    )

    await db.commit()

    # Get last message
    last_message = await get_last_message_for_session(db, session)

    # Get hotels
    hotels = await get_hotels_for_session(db, session)
    formatted_hotels = [HotelResponse.from_orm(hotel) for hotel in hotels]

    # Format session response
    session_response = SessionResponse.from_orm(session)

    return SessionWithHotelsResponse(
        **session_response.model_dump(),
        message=last_message.text if last_message else None,
        hotels=formatted_hotels,
        all_vibes=[],  # TODO: Return session vibes
    )
