from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from db.database import Base


class ChatLog(Base):
    __tablename__ = "chat_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), ForeignKey("google_oauth.email"))
    query = Column(String(5000))
    answer = Column(String(5000))
    created_at = Column(DateTime, default=datetime.now)
