from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from ..models import user as user_model


def get_user_info(db: Session, username: str):
    """
    유저 정보 조회

    Args:
        db (Session):
        username (str):

    Returns:
        user_model.User:

    """
    stmt = select(user_model.User).where(user_model.User.username == username)
    result = db.execute(stmt).scalar_one_or_none()
    return result
