from pydantic import BaseModel
from datetime import datetime

class LogSchema(BaseModel):
    description: str
    user_id: int
    change_type: str
    created_at: datetime

class ErrorResponse(BaseModel):
    message: str
    status_code: int
