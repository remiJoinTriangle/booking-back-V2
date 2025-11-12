from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import (
    CreateSessionParameters,
    SessionResponse,
    SessionWithHotelsResponse,
)
from ...services.session_service import (
    add_message_to_session,
    create_message,
    create_session,
)

# TODO: Define message types and vibes constants

router = APIRouter(prefix="/session", tags=["session"])


@router.post("", response_model=SessionWithHotelsResponse)
async def start_session(
    arguments: CreateSessionParameters,
    db: AsyncSession = Depends(get_db),
):
    try:
        session_obj = await create_session(
            db=db,
            owner_id=1,
            message=arguments.message,
            enriched_prompt=arguments.enriched_prompt or "",
        )

        today = session_obj.start_day
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        current_month = months[session_obj.start_month - 1]

        date_message = await create_message(
            db=db,
            message_type=3,
            text=f"Today is the {today} of {current_month} {session_obj.start_year}",
        )

        await add_message_to_session(db, session_obj, date_message)

        user_message = await create_message(
            db=db,
            message_type=2,
            text=arguments.message,
        )

        await add_message_to_session(db, session_obj, user_message)

        await db.flush()
        await db.commit()

        await db.refresh(session_obj)

        session_response = SessionResponse.from_orm(session_obj)

        return SessionWithHotelsResponse(
            **session_response.model_dump(),
            message=None,
            hotels=[],
            all_vibes=[],
        )

    except Exception as e:
        await db.rollback()
        raise e
