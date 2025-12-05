from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.database import Base


class ChatLog(Base):
    __tablename__ = "chat_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), ForeignKey("google_oauth.email"))
    query = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
