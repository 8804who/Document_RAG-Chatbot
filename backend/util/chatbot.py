from core import config
from crud import chat_log as chat_log_crud
from db.database import get_async_db_session

LANGSMITH_TRACING=config.LANGSMITH_TRACING
LANGSMITH_ENDPOINT=config.LANGSMITH_ENDPOINT
LANGSMITH_API_KEY=config.LANGSMITH_API_KEY
LANGSMITH_PROJECT=config.LANGSMITH_PROJECT


async def save_chat_log(email: str, query: str, answer: str) -> None:
    """
    유저 채팅 로그 저장

    Args:
        email: 유저 이메일
        query: 유저 메시지
        answer: 챗봇 응답

    Returns:
        None
    """
    try:
        async with get_async_db_session() as db:
            await chat_log_crud.save_chat_log(db, email, query, answer)
    except Exception as e:
        raise e
