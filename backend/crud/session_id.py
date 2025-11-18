from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert as pg_insert
from typing import Optional

from models.session_id import SessionId
from util.logger import logger


def save_session_id(db: Session, email: str, session_id: str) -> None:
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
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving session id: {e}")
        raise e


def get_session_id(db: Session, email: str) -> Optional[SessionId]:
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
        return db.execute(stmt).scalar_one_or_none()
    except Exception as e:
        logger.error(f"Error getting session id: {e}")
        raise e
