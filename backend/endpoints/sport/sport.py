from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.serializers.sport import SportResponse
from backend.services.sport_service import get_sport_by_id, get_sports


router = APIRouter(prefix="/sport", tags=["sport"])


@router.get("/", response_model=list[SportResponse])
async def retrieve_all_sports(db: AsyncSession = Depends(get_db)):
    sports = await get_sports(db)
    return [SportResponse.from_orm(sport) for sport in sports]


@router.get("/{id}", response_model=SportResponse)
async def retrieve_sport(id: int, db: AsyncSession = Depends(get_db)):
    sport = await get_sport_by_id(db, id)
    return SportResponse.from_orm(sport)

