from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from ..models import Session, Hotel


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
