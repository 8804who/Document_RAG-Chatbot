from models.chat_history import ChatHistory
from sqlalchemy import insert
from sqlalchemy.orm import Session


def save_chat_history(db: Session, session_id: str, context: str) -> None:
    """
    session_id를 통해 채팅 히스토리 저장

    Args:
        db: 데이터베이스 세션
        session_id: 세션 아이디
        context: 채팅 히스토리
    """
    try:
        stmt = insert(ChatHistory).values(session_id=session_id, context=context)
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def get_chat_history(db: Session, session_id: str) -> ChatHistory:
    """
    session_id를 통해 채팅 히스토리 조회

    Args:
        db: 데이터베이스 세션
        session_id: 세션 아이디

    Returns:
        ChatHistory: 채팅 히스토리
    """
    try:
        return db.query(ChatHistory).filter(ChatHistory.session_id == session_id).first()
    except Exception as e:
        raise e