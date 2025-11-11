from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.serializers.activity import ActivityResponse
from backend.services.activity_service import get_activities, get_activity_by_id

router = APIRouter(prefix="/activity", tags=["activity"])


@router.get("/", response_model=list[ActivityResponse])
async def retrieve_all_activities(db: AsyncSession = Depends(get_db)):
    activities = await get_activities(db)
    return [ActivityResponse.from_orm(activity) for activity in activities]


@router.get("/{id}", response_model=ActivityResponse)
async def retrieve_activity(id: int, db: AsyncSession = Depends(get_db)):
    activity = await get_activity_by_id(db, id)
    return ActivityResponse.from_orm(activity)
