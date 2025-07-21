from pydantic import BaseModel
from datetime import datetime


class ChatLog(BaseModel):
    username: str
    query: str
    response: str
    created_at: datetime
