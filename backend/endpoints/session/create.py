from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import CreateSessionParameters, SessionWithHotelsResponse, SessionResponse, HotelResponse
from ...services.session_service import (
    create_session,
    create_message,
    add_message_to_session,
)
# TODO: Define message types and vibes constants

router = APIRouter(prefix="/session", tags=["session"])


@router.post("", response_model=SessionWithHotelsResponse)
async def start_session(
    arguments: CreateSessionParameters,
    background: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session - Start a new session.
    """
    # TODO: Implement authentication
    # TODO: Trigger background LLM processing

    session = await create_session(
        db=db,
        owner_id=1,  # Stub. TODO: Get actual user ID from authentication
        message=arguments.message,
        enriched_prompt=arguments.enrichedPrompt or "",
    )

    # Add initial message with date of the day
    # FIXME: use a date library
    today = session.start_day
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    current_month = months[session.start_month - 1]
    date_message = await create_message(
        db=db,
        message_type=3,  # 3 = MESSAGE_TYPE_ASSISTANT. TODO: Use proper message type enum/table
        text=f"Today is the {today} of {current_month} {session.start_year}",
    )
    await add_message_to_session(db, session, date_message)

    # Add user message
    user_message = await create_message(
        db=db,
        message_type=2,  # 2 = MESSAGE_TYPE_USER. TODO: Use proper message type enum/table
        text=arguments.message,
    )
    await add_message_to_session(db, session, user_message)
    await db.commit()

    # Format session response
    session_response = SessionResponse.from_orm(session)

    # TODO: Get all vibes list
    return SessionWithHotelsResponse(
        **session_response.model_dump(),
        message=None,
        hotels=[],  # New sessions have no hotels yet
        allVibes=[],  # TODO: Return all vibes
    )
