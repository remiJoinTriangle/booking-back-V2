from fastapi import APIRouter

from .hotel.get import router as hotel_get_router
from .session.create import router as session_create_router
from .session.list import router as session_list_router
from .session.get import router as session_get_router
from .session.message import router as session_message_router
from .session.date import router as session_date_router
from .session.filters import router as session_filters_router
from .session.hotel import router as session_hotel_router

# Create main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(hotel_get_router)
api_router.include_router(session_create_router)
api_router.include_router(session_list_router)
api_router.include_router(session_get_router)
api_router.include_router(session_message_router)
api_router.include_router(session_date_router)
api_router.include_router(session_filters_router)
api_router.include_router(session_hotel_router)

__all__ = ["api_router"]

