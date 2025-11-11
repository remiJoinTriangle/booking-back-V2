from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Activity


async def get_activities(db: AsyncSession) -> list[Activity]:
    result = await db.execute(select(Activity))
    return list(result.scalars().all())


async def get_activity_by_id(db: AsyncSession, id: int) -> Activity | None:
    result = await db.execute(select(Activity).where(Activity.id == id))
    return result.scalar_one_or_none()
