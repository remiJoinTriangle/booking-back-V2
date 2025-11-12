from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import Hotel
from backend.services.agentic.serializers import HotelFilter


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

    if filters.cities:
        city_filters = [
            and_(
                Hotel.latitude.between(city[0] - 0.15, city[0] + 0.15),
                Hotel.longitude.between(city[1] - 0.15, city[1] + 0.15),
            )
            for city in filters.cities
        ]
        query = query.filter(or_(*city_filters))
    return query
