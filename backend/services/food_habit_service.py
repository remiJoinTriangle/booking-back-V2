from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import FoodHabit


async def get_food_habits(db: AsyncSession) -> list[FoodHabit]:
    result = await db.execute(select(FoodHabit))
    return list(result.scalars().all())


async def get_food_habit_by_id(db: AsyncSession, id: int) -> FoodHabit | None:
    result = await db.execute(select(FoodHabit).where(FoodHabit.id == id))
    return result.scalar_one_or_none()
