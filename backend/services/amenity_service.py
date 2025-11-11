from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Amenity


async def get_amenities(db: AsyncSession) -> list[Amenity]:
    result = await db.execute(select(Amenity))
    return list(result.scalars().all())


async def get_amenity_by_id(db: AsyncSession, id: int) -> Amenity | None:
    result = await db.execute(select(Amenity).where(Amenity.id == id))
    return result.scalar_one_or_none()
