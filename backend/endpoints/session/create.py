from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import CreateSessionParameters, SessionWithHotelsResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.post("", response_model=SessionWithHotelsResponse)
async def start_session(
    arguments: CreateSessionParameters = None,
    background: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session - Start a new session.
    """
    # TODO: Implement authentication
    # TODO: Validate message parameter
    # TODO: Create session with default dates
    # TODO: Create initial messages
    # TODO: Return session.to_front() format with hotels=[], allVibes=ALL_VIBES

    if not arguments or not arguments.message:
        return ORJSONResponse(
            status_code=400,
            content={"errorMessage": "[message] in JSON body is missing"}
        )

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
