from models.chat_log import ChatLog
from sqlalchemy import insert
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession


async def save_chat_log(db: AsyncSession, email: str, query: str, answer: str) -> None:
    """
    유저 채팅 로그 저장

    Args:
        db: CRUD를 수행할 DB 세션
        email: 유저 이메일
        query: 유저 메시지
        answer: 챗봇 응답

    Returns:
        None
    """
    try:
        stmt = insert(ChatLog).values(email=email, query=query, answer=answer)
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
