from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import (
    AddSessionMessageParameters,
    HotelResponse,
    MessageResponse,
    SessionResponse,
    SessionWithHotelsResponse,
)
from ...services.agentic.graph import workflow
from ...services.session_service import (
    add_message_to_session,
    create_message,
    get_hotels_for_session,
    get_last_message_for_session,
    get_messages_for_session,
    get_session_by_id,
    update_session_status,
)

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/message", response_model=SessionWithHotelsResponse)
async def post_message(
    session_id: int,
    arguments: AddSessionMessageParameters,
    background: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
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
        raise HTTPException(
            status_code=404, detail=f"Session [{session_id}] does not exist"
        )

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
        all_vibes=[],  # TODO: Return all vibes
    )


@router.get("/{session_id}/message", response_model=List[MessageResponse])
async def get_message(session_id: int, db: AsyncSession = Depends(get_db)):
    """
    GET /session/{session_id}/message - Get a message from a session.
    """
    session = await get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=404, detail=f"Session [{session_id}] does not exist"
        )

    # Get messages
    messages = await get_messages_for_session(session, db)
    formatted_messages = [
        MessageResponse.model_validate(message) for message in messages
    ]

    return formatted_messages


@router.post("/{session_id}/message/agentic", response_model=MessageResponse)
async def post_message_agentic(
    session_id: int,
    arguments: AddSessionMessageParameters,
    background: BackgroundTasks = BackgroundTasks(),
    db: AsyncSession = Depends(get_db),
):
    """
    POST /session/{session_id}/message/agentic - Add a message to a session using agentic processing.
    """
    initial_state = {"input": arguments.message}
    result = await workflow.ainvoke(initial_state)  # type: ignore[arg-type]
    return JSONResponse(
        content={
            "message": result.get("route"),
            "action": result.get("action"),
            "reformulated": result.get("reformulated"),
            # "filters": result.get("filters").model_dump(),
            # "hotels": [hotel.model_dump() for hotel in result.get("hotels")],
        }
    )
