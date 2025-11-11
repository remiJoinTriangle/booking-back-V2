from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.serializers.food_habit import FoodHabitResponse
from backend.services.food_habit_service import (
    get_food_habit_by_id,
    get_food_habits,
)

router = APIRouter(prefix="/food-habit", tags=["food_habit"])


@router.get("/", response_model=list[FoodHabitResponse])
async def retrieve_all_food_habits(db: AsyncSession = Depends(get_db)):
    food_habits = await get_food_habits(db)
    return [FoodHabitResponse.from_orm(food_habit) for food_habit in food_habits]


@router.get("/{id}", response_model=FoodHabitResponse)
async def retrieve_food_habit(id: int, db: AsyncSession = Depends(get_db)):
    food_habit = await get_food_habit_by_id(db, id)
    return FoodHabitResponse.from_orm(food_habit)
