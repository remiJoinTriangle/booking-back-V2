from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ...database import get_db
from ...serializers import HttpPostSessionMessageArguments, SessionWithHotelsResponse, ErrorResponse

router = APIRouter(prefix="/session", tags=["session"])


@router.post("/{session_id}/message", response_model=SessionWithHotelsResponse)
async def add_message_to_session(
    session_id: int,
    arguments: HttpPostSessionMessageArguments,
    background: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db)
):
    """
    POST /session/{session_id}/message - Add a message to a session.
    """
    # TODO: Implement authentication
    # TODO: Validate message parameter
    # TODO: Check session ownership
    # TODO: Create message and add to session
    # TODO: Update session status
    # TODO: Trigger background LLM processing
    # TODO: Return session.to_front() format with message, hotels, allVibes

    if not arguments.message:
        return ORJSONResponse(
            status_code=400,
            content={"errorMessage": "[message] in JSON body is missing"}
        )

    return ORJSONResponse(
        status_code=501,
        content={"errorMessage": "Endpoint not implemented"}
    )
