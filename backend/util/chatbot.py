from crud import chat_log as chat_log_crud
from db.database import get_db


def save_chat_log(email: str, query: str, response: str) -> None:
    """
    유저 채팅 로그 저장

    Args:
        email: 유저 이메일
        query: 유저 메시지
        response: 챗봇 응답

    Returns:
        None
    """
    try:
        db = next(get_db())
        chat_log_crud.save_chat_log(db, email, query, response)
    except Exception as e:
        raise e
