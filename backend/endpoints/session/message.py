from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import AddSessionMessageParameters, SessionWithHotelsResponse, SessionResponse, HotelResponse
from ...services.session_service import (
    get_session_by_id,
    create_message,
    add_message_to_session,
    get_last_message_for_session,
    update_session_status,
    get_hotels_for_session,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/message", response_model=SessionWithHotelsResponse)
async def post_message(
    session_id: int,
    arguments: AddSessionMessageParameters,
    background: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session/{session_id}/message - Add a message to a session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Trigger background LLM processing

    if not arguments.message:
        raise HTTPException(status_code=400, detail="[message] in JSON body is missing")

    # Get session
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session [{session_id}] does not exist")

    # Create user message
    user_message = await create_message(
        db=db,
        message_type=2,  # 2 = MESSAGE_TYPE_USER. TODO: Use proper message type enum/table
        text=arguments.message,
    )
    await add_message_to_session(db, session, user_message)

    # Update session status
    # TODO: Use proper session status enum/table
    await update_session_status(db, session, 6)  # 6 = SESSION_STATUS_WORKING_MESSAGE

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
        allVibes=[],  # TODO: Return all vibes
    )
