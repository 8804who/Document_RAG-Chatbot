from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatLog(Base):
    __tablename__ = "chat_log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), ForeignKey("google_oauth.email"))
    query = Column(String(500))
    answer = Column(String(500))
    created_at = Column(DateTime, default=datetime.now)
