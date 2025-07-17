from pydantic import BaseModel
from datetime import datetime


class ChatLog(BaseModel):
    user_id: str
    message: str
    response: str
    created_at: datetime
