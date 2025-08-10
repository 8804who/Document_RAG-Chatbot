from models.auth import GoogleOauth
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
        db_google_oauth = GoogleOauth(
            name=name, email=email, refresh_token=refresh_token
        )
        db.add(db_google_oauth)
        db.commit()
        db.refresh(db_google_oauth)
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
        return db.query(GoogleOauth).filter(GoogleOauth.email == email).first()
    except Exception as e:
        raise e
