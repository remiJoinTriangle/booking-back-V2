from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import Hotel


async def get_hotel_by_id(db: AsyncSession, hotel_id: int) -> Hotel | None:
    """Get a single hotel by ID."""
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    return result.scalar_one_or_none()
