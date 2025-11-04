from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HotelDetailResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/{session_id}/hotel/{hotel_id}", response_model=HotelDetailResponse)
async def get_session_hotel_detail(
    session_id: int,
    hotel_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    GET /session/{session_id}/hotel/{hotel_id} - Get hotel page for a given session.
    """
    # TODO: Implement authentication
    # TODO: Check session ownership
    # TODO: Load hotel with reviews and assets
    # TODO: Format reviews with avatar, date, rating
    # TODO: Format images and main image
    # TODO: Return hotel data with matching flags, dates, highlights, etc.

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
