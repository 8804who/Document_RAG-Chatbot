from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ChatHistory(Base):
    __tablename__ = "chat_history"
    session_id = Column(String(255), primary_key=True)
    context = Column(String(10000))