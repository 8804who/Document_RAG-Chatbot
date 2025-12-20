from sqlalchemy import Column, ForeignKey, String

from app.db.database import Base


class SessionId(Base):
    __tablename__ = "session_id"
    email = Column(
        String(100), ForeignKey("google_oauth.email"), primary_key=True
    )
    session_id = Column(String(100))
