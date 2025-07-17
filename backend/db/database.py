from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core import config
from sqlalchemy.orm import Session
from typing import Generator

DB_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()


def get_db() -> Generator[Session, None, None]:
    """
    DB 세션 생성

    Returns:
        Generator[Session, None, None]: DB 세션 생성 및 반환, 사용 후 세션 종료
    """
    try:
        yield db
    finally:
        db.close()
