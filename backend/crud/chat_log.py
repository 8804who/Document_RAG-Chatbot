from models.chat_log import ChatLog
from sqlalchemy import insert
from sqlalchemy.orm import Session


def save_chat_log(db: Session, email: str, query: str, response: str) -> None:
    """
    유저 채팅 로그 저장

    Args:
        db: CRUD를 수행할 DB 세션
        email: 유저 이메일
        query: 유저 메시지
        response: 챗봇 응답

    Returns:
        None
    """
    try:
        stmt = insert(ChatLog).values(email=email, query=query, response=response)
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
