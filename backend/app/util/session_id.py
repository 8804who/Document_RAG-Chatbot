import uuid

from app.crud import session_id as session_id_crud
from app.db.database import get_async_db_session
from app.util.logger import logger


async def session_id_management(email: str) -> str:
    """
    Session ID 관리

    Args:
        email: The email of the user.

    Returns:
        str: The session ID.
    """
    session_id = await get_session_id(email)
    if session_id is None:
        session_id = str(uuid.uuid4())
        await save_session_id(email, session_id)
    return session_id


async def save_session_id(email: str, session_id: str) -> None:
    """
    Session ID 저장

    Args:
        email: The email of the user.
        session_id: The session ID.
    """
    try:
        async with get_async_db_session() as db:
            await session_id_crud.save_session_id(
                db=db, email=email, session_id=session_id
            )
    except Exception as e:
        logger.error(f"Error saving session id: {e}")


async def get_session_id(email: str) -> str | None:
    """
    Session ID 조회

    Args:
        email: The email of the user.

    Returns:
        str | None: The session ID, or None if not found or on error.
    """
    try:
        async with get_async_db_session() as db:
            result = await session_id_crud.get_session_id(db=db, email=email)
        return result.session_id if result else None
    except Exception as e:
        logger.error(f"Error getting session id: {e}")
        return None
