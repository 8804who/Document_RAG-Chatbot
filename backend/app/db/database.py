from contextlib import contextmanager, asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import Settings

Base = declarative_base()

DB_URL = f"postgresql://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}"
ASYNC_DB_URL = f"postgresql+asyncpg://{Settings.DB_USER}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_NAME}"

engine = create_engine(DB_URL)
async_engine = create_async_engine(ASYNC_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)


@contextmanager
def get_db_session() -> Session:
    """
    DB 세션 생성

    Returns:
        Generator[Session, None, None]: DB 세션 생성 및 반환, 사용 후 세션 종료
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@asynccontextmanager
async def get_async_db_session() -> AsyncSession:
    """
    DB 세션 생성

    Returns:
        Generator[AsyncSession, None, None]: DB 세션 생성 및 반환, 사용 후 세션 종료
    """
    async with AsyncSessionLocal() as db:
        yield db
