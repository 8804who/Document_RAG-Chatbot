from app.core.config import settings
from app.crud import chat_log as chat_log_crud
from app.db.database import get_async_db_session

LANGSMITH_TRACING = settings.LANGSMITH_TRACING
LANGSMITH_ENDPOINT = settings.LANGSMITH_ENDPOINT
LANGSMITH_API_KEY = settings.LANGSMITH_API_KEY
LANGSMITH_PROJECT = settings.LANGSMITH_PROJECT


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
