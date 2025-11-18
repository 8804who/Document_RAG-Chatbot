from sqlalchemy import Column, String, ForeignKey

from db.database import Base


class SessionId(Base):
    __tablename__ = "session_id"
    email = Column(String(255), ForeignKey("google_oauth.email"), primary_key=True)
    session_id = Column(String(255))
