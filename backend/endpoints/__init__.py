from fastapi import APIRouter

from .activity.activity import router as activity_router
from .food_habit.food_habit import router as food_habit_router
from .hotel.get import router as hotel_get_router
from .session.create import router as session_create_router
from .session.date import router as session_date_router
from .session.filters import router as session_filters_router
from .session.get import router as session_get_router
from .session.hotel import router as session_hotel_router
from .session.list import router as session_list_router
from .session.message import router as session_message_router
from .sport.sport import router as sport_router
from .user.user import router as user_router

# Create main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(activity_router)
api_router.include_router(food_habit_router)
api_router.include_router(sport_router)
api_router.include_router(hotel_get_router)
api_router.include_router(session_create_router)
api_router.include_router(session_list_router)
api_router.include_router(session_get_router)
api_router.include_router(session_message_router)
api_router.include_router(session_date_router)
api_router.include_router(session_filters_router)
api_router.include_router(session_hotel_router)
api_router.include_router(user_router)

__all__ = ["api_router"]
