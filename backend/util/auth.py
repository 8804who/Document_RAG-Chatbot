from crud import auth as auth_crud
from db.database import get_db


def save_google_oauth_token(name: str, email: str, refresh_token: str) -> None:
    """
    Save the Google OAuth token to the database.

    Args:
        name: The name of the user.
        email: The email of the user.
        refresh_token: The refresh token of the user.

    Returns:
        None
    """
    try:
        db = next(get_db())
        auth_crud.save_google_oauth_token(db, name, email, refresh_token)
    except Exception as e:
        raise e


def get_google_oauth_token(email: str) -> str:
    """
    Get the Google OAuth token from the database.

    Args:
        email: The email of the user.

    Returns:
        str: The Google OAuth token.
    """
    try:
        db = next(get_db())
        return auth_crud.get_google_oauth_token(db, email)
    except Exception as e:
        raise e
