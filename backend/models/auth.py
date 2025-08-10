from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GoogleOauth(Base):
    __tablename__ = "google_oauth"
    email = Column(String(255), primary_key=True)
    name = Column(String(255))
    refresh_token = Column(String(255))
