from sqlalchemy import Column, DateTime, ForeignKey, INTEGER, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Chat_log(Base):
    __tablename__ = "chat_log_table"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(String(20), ForeignKey("user_table.username"))
    query = Column(String(500))
    response = Column(String(500))
    created_at = Column(DateTime)
