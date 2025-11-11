from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.serializers.amenity import AmenityResponse
from backend.services.amenity_service import get_amenities, get_amenity_by_id

router = APIRouter(prefix="/amenity", tags=["amenity"])


@router.get("/", response_model=list[AmenityResponse])
async def retrieve_all_amenities(db: AsyncSession = Depends(get_db)):
    amenities = await get_amenities(db)
    return [AmenityResponse.from_orm(amenity) for amenity in amenities]


@router.get("/{id}", response_model=AmenityResponse)
async def retrieve_amenity(id: int, db: AsyncSession = Depends(get_db)):
    amenity = await get_amenity_by_id(db, id)
    return AmenityResponse.from_orm(amenity)
