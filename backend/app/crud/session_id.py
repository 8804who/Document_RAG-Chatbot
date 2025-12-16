from typing import Optional

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session_id import SessionId
from app.util.logger import logger


async def save_session_id(
    db: AsyncSession, email: str, session_id: str
) -> None:
    """
    email를 통해 세션 아이디 저장

    Args:
        db: 데이터베이스 세션
        session_id: 세션 아이디
    """
    try:
        stmt = (
            pg_insert(SessionId)
            .values(email=email, session_id=session_id)
            .on_conflict_do_update(
                index_elements=["email"],
                set_={"session_id": session_id},
            )
        )
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Error saving session id: {e}")
        raise e


async def get_session_id(db: AsyncSession, email: str) -> Optional[SessionId]:
    """
    email를 통해 세션 아이디 조회

    Args:
        db: 데이터베이스 세션
        email: 유저 이메일

    Returns:
        SessionId: 세션 아이디
    """
    try:
        stmt = select(SessionId).where(SessionId.email == email)
        return (await db.execute(stmt)).scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting session id: {e}")
        raise e
