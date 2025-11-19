import uuid

from crud import session_id as session_id_crud
from db.database import get_db_session


def session_id_management(email: str) -> str:
    """
    Session ID 관리

    Args:
        email: The email of the user.

    Returns:
        str: The session ID.
    """
    session_id = get_session_id(email)
    if session_id is None:
        session_id = str(uuid.uuid4())
        save_session_id(email, session_id)
    return session_id


def save_session_id(email: str, session_id: str) -> None:
    """
    Session ID 저장

    Args:
        db: Database session
        email: The email of the user.
        session_id: The session ID.
    """
    with get_db_session() as db:
        session_id_crud.save_session_id(db, email, session_id)


def get_session_id(email: str) -> str:
    """
    Session ID 조회

    Args:
        db: Database session
        email: The email of the user.

    Returns:
        str: The session ID.
    """
    with get_db_session() as db:
        result = session_id_crud.get_session_id(db, email)
    return result.session_id if result else None
