from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Hotel
from backend.serializers.hotel import HotelFilter


async def get_hotel_by_id(db: AsyncSession, hotel_id: int) -> Hotel | None:
    """Get a single hotel by ID."""
    result = await db.execute(select(Hotel).where(Hotel.id == hotel_id))
    return result.scalar_one_or_none()


def apply_filters(query, filters: HotelFilter):
    """Transform a Pydantic filter model into SQLAlchemy filters."""
    if filters.min_price is not None:
        query = query.filter(Hotel.price >= filters.min_price)

    if filters.max_price is not None:
        query = query.filter(Hotel.price <= filters.max_price)

    if filters.min_stars is not None:
        query = query.filter(Hotel.star_rating >= filters.min_stars)

    if filters.max_stars is not None:
        query = query.filter(Hotel.star_rating <= filters.max_stars)

    return query
