from pydantic import BaseModel


class ErrorResponse(BaseModel):
    errorMessage: str
