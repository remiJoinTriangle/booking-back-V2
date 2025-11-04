from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import ErrorResponse

router = APIRouter(prefix="/hotel", tags=["hotel"])


@router.get("/{id}", response_model=ErrorResponse)
async def get_hotel(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a single hotel by ID.
    """
    # TODO: Implement authentication
    # TODO: Implement hotel retrieval logic

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
