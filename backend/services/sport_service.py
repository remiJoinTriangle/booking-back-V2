from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Sport


async def get_sports(db: AsyncSession) -> list[Sport]:
    result = await db.execute(select(Sport))
    return list(result.scalars().all())


async def get_sport_by_id(db: AsyncSession, id: int) -> Sport | None:
    result = await db.execute(select(Sport).where(Sport.id == id))
    return result.scalar_one_or_none()

