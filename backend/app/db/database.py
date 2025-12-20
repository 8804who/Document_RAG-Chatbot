from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from app.core.config import settings

Base = declarative_base()

ASYNC_DB_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

async_engine = create_async_engine(ASYNC_DB_URL)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)


@asynccontextmanager
async def get_async_db_session() -> AsyncSession:
    """
    DB 세션 생성

    Returns:
        Generator[AsyncSession, None, None]: DB 세션 생성 및 반환, 사용 후 세션 종료
    """
    async with AsyncSessionLocal() as db:
        yield db
