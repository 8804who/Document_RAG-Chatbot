from sqlalchemy import Column, String

from db.database import Base


class GoogleOauth(Base):
    __tablename__ = "google_oauth"
    email = Column(String(255), primary_key=True)
    name = Column(String(255))
    refresh_token = Column(String(255))
