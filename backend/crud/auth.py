from models.auth import GoogleOauth
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session


def save_google_oauth_token(
    db: Session, name: str, email: str, refresh_token: str
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
        db.execute(stmt)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e


def get_google_oauth_token(db: Session, email: str) -> str:
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
        return db.execute(stmt).first()
    except Exception as e:
        raise e
