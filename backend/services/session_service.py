import time
from datetime import datetime, timedelta
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import Hotel, Message, Session


async def get_sessions(db: AsyncSession, limit: int = 5) -> List[Session]:
    """Get all sessions."""
    result = await db.execute(select(Session).limit(limit))
    return list(result.scalars().all())


async def get_session_by_id(db: AsyncSession, session_id: int) -> Session | None:
    """Get a single session by ID."""
    result = await db.execute(select(Session).where(Session.id == session_id))
    return result.scalar_one_or_none()


async def get_hotels_for_session(db: AsyncSession, session: Session) -> List[Hotel]:
    """Get all hotels for a session."""
    result = await db.execute(select(Hotel))
    return list(result.scalars().all())


async def create_session(
    db: AsyncSession,
    owner_id: int,
    message: str,
    enriched_prompt: str = "",
) -> Session:
    """Create a new session."""
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year

    # TODO: use a better nested object for dates instead of all those attributes at root-level
    next_week = today + timedelta(days=7)
    next_week_day = next_week.day
    next_week_month = next_week.month
    next_week_year = next_week.year

    current_time = int(time.time())

    # TODO: use null values instead of harcoded defaults values (-1 but also lat/long, 0, etc.)
    session = Session(
        name="new session",
        status=5,  # 5 = SESSION_STATUS_WORKING_MAP. TODO: Use proper session status enum/table
        longitude=2.3376,  # By default, use Paris coordinates.
        latitude=48.8606,
        zoom=10,
        last_interacted=current_time,
        start_day=day,
        end_day=next_week_day,
        start_month=month,
        end_month=next_week_month,
        start_year=year,
        end_year=next_week_year,
        owner_id=owner_id,
        flag=0,
        vibes="",
        price=-1,
        count_of_room=-1,
        user_prompt=message,
        vibe_flag=0,
        packed_date=0,
        enriched_prompt=enriched_prompt,
        initial_min_price=-1,
        initial_max_price=-1,
        filter_min_price=-1,
        filter_max_price=-1,
        min_star_rating=-1,
        min_review_rating=-1.0,
        number_of_rooms={},
    )

    db.add(session)
    await db.flush()
    await db.refresh(session)

    return session


async def create_message(
    db: AsyncSession,
    message_type: int,
    text: str,
) -> Message:
    """Create a new message."""
    message = Message(
        type=message_type,
        text=text,
        function_name="",
        function_argument_string="",
        tool_id="",
    )

    db.add(message)
    await db.flush()
    await db.refresh(message)

    return message


async def add_message_to_session(
    db: AsyncSession,
    session: Session,
    message: Message,
) -> None:
    """Add a message to a session."""
    session.messages.append(message)
    session.last_interacted = int(time.time())
    await db.flush()


async def get_last_message_for_session(
    db: AsyncSession,
    session: Session,
) -> Optional[Message]:
    """Get the last message for a session."""
    # Load messages relationship
    # FIXME: load only the last message
    await db.refresh(session, ["messages"])
    if session.messages:
        return max(session.messages, key=lambda m: m.id)
    return None


async def update_session_dates(
    db: AsyncSession,
    session: Session,
    start_day: int,
    end_day: int,
    start_month: int,
    end_month: int,
    start_year: int,
    end_year: int,
) -> Session:
    """Update session dates."""
    # TODO: remove those -1 checks once we have proper null values
    session.start_day = start_day if start_day != -1 else session.start_day
    session.end_day = end_day if end_day != -1 else session.end_day
    session.start_month = start_month if start_month != -1 else session.start_month
    session.end_month = end_month if end_month != -1 else session.end_month
    session.start_year = start_year if start_year != -1 else session.start_year
    session.end_year = end_year if end_year != -1 else session.end_year
    session.last_interacted = int(time.time())

    await db.flush()
    await db.refresh(session)

    return session


async def update_session_filters(
    db: AsyncSession,
    session: Session,
    filters: dict,
) -> Session:
    """Update session filters."""
    # TODO: Clean those -1 comparisons up once we have proper null values
    if filters.get("price") != -1:
        session.price = filters["price"]
    if filters.get("minPrice") != -1:
        session.filter_min_price = filters["minPrice"]
    if filters.get("maxPrice") != -1:
        session.filter_max_price = filters["maxPrice"]
    if filters.get("minStarRating") != -1:
        session.min_star_rating = filters["minStarRating"]
    if filters.get("minReviewRating") != -1:
        session.min_review_rating = filters["minReviewRating"]

    # TODO: update amenities and vibes once we have proper Amenities/Vibes tables

    session.last_interacted = int(time.time())

    await db.flush()
    await db.refresh(session)

    return session


async def update_session_status(
    db: AsyncSession,
    session: Session,
    status: int,
) -> Session:
    """Update session status."""
    session.status = status
    await db.flush()
    await db.refresh(session)
    return session


async def get_messages_for_session(
    session: Session,
    db: AsyncSession,
    limit: int = 10,
) -> List[Message]:
    """Get the last message for a session."""
    await db.refresh(session, ["messages"])
    if session.messages:
        return session.messages[-limit:]
    return []
