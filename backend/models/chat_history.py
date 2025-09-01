from sqlalchemy import Column, String, Text
from db.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"
    session_id = Column(String(255), primary_key=True)
    context = Column(Text)