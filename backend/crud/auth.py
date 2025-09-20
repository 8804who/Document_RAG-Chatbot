from models.auth import GoogleOauth
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from util.logger import logger


async def save_google_oauth_token(
    db: AsyncSession, name: str, email: str, refresh_token: str
) -> None:
    """
    Save the Google OAuth token to the database.

    Args:
        db: The database session.
        name: The name of the user.
        email: The email of the user.
        refresh_token: The refresh token of the user.

    Returns:
        None
    """
    try:
        stmt = (
            insert(GoogleOauth)
            .values(name=name, email=email, refresh_token=refresh_token)
            .on_conflict_do_update(
                index_elements=["email"],
                set_={"name": name, "refresh_token": refresh_token},
            )
        )
        await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        logger.error(f"Error saving Google OAuth token: {e}")
        raise e


async def get_google_oauth_token(db: AsyncSession, email: str) -> str:
    """
    Get the Google OAuth token from the database.

    Args:
        db: The database session.
        email: The email of the user.

    Returns:
        str: The Google OAuth token.
    """
    try:
        stmt = select(GoogleOauth).where(GoogleOauth.email == email)
        return (await db.execute(stmt)).first()
    except Exception as e:
        logger.error(f"Error getting Google OAuth token: {e}")
        raise e
