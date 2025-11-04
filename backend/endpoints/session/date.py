from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import UpdateSessionDateParameters, SessionWithHotelsResponse, SessionResponse, HotelResponse
from ...services.session_service import (
    get_session_by_id,
    update_session_dates,
    get_last_message_for_session,
    get_hotels_for_session,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/date", response_model=SessionWithHotelsResponse)
async def change_date_of_session(
    session_id: int,
    arguments: UpdateSessionDateParameters,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session/{session_id}/date - Change date of a session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Update session date (packed_date format)

    # Get session
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session [{session_id}] does not exist")

    # Update session dates
    session = await update_session_dates(
        db=db,
        session=session,
        start_day=arguments.startDay,
        end_day=arguments.endDay,
        start_month=arguments.startMonth,
        end_month=arguments.endMonth,
        start_year=arguments.startYear,
        end_year=arguments.endYear,
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
        allVibes=[],  # TODO: Return session vibes
    )
