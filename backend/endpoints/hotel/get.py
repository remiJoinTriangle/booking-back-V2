from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HotelResponse
from ...services.hotel_service import get_hotel_by_id

router = APIRouter(prefix="/hotel", tags=["hotel"])


@router.get("/{id}", response_model=HotelResponse)
async def get_hotel(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single hotel by ID.
    """
    # TODO: Implement authentication

    hotel = await get_hotel_by_id(db, id)
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")

    return HotelResponse.from_orm(hotel)
