from datetime import datetime

from pydantic import BaseModel


class ChatLog(BaseModel):
    username: str
    query: str
    answer: str
    created_at: datetime
