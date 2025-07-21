from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "user_table"
    username = Column(String(20), primary_key=True)
    password = Column(String(60), nullable=False)
    email = Column(String(20), nullable=False)
