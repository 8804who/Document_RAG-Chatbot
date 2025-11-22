from fastapi import HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import httpx

from app.core import config
from app.crud import auth as auth_crud
from app.db.database import get_async_db_session
from app.util.logger import logger

GOOGLE_CLIENT_ID = config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = config.GOOGLE_CLIENT_SECRET


async def save_google_oauth_token(name: str, email: str, refresh_token: str) -> None:
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
        async with get_async_db_session() as db:
            await auth_crud.save_google_oauth_token(db, name, email, refresh_token)
    except Exception as e:
        raise e


async def get_google_oauth_token(email: str) -> str:
    """
    Get the Google OAuth token from the database.

    Args:
        email: The email of the user.

    Returns:
        str: The Google OAuth token.
    """
    try:
        async with get_async_db_session() as db:
            return await auth_crud.get_google_oauth_token(db, email)
    except Exception as e:
        raise e


async def verify_google_token(token: str) -> dict:
    """
    Google에서 발급받은 access_token 인증

    Args:
        token (str): 인증받을 토큰

    Returns:
        dict: 토큰 정보
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?access_token={token}"
            )

        if response.status_code == 200:
            token_info = response.json()

            if token_info.get("aud") != GOOGLE_CLIENT_ID:
                raise HTTPException(status_code=401, detail="Invalid token audience")

            return {
                "valid": True,
                "user_info": {
                    "email": token_info.get("email"),
                    "name": token_info.get("name"),
                    "picture": token_info.get("picture"),
                    "sub": token_info.get("sub"),
                },
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid token")

    except httpx.RequestException as e:
        logger.error(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Token verification failed")


async def verify_google_id_token(id_token_str: str) -> dict:
    """
    Google ID Token 인증

    Args:
        id_token_str (str):

    Returns:
        dict: 토큰 정보

    """
    try:
        idinfo = id_token.verify_oauth2_token(
            id_token_str, google_requests.Request(), GOOGLE_CLIENT_ID
        )
        return {
            "valid": True,
            "user_info": {
                "email": idinfo.get("email"),
                "name": idinfo.get("name"),
                "picture": idinfo.get("picture"),
                "sub": idinfo.get("sub"),
            },
        }

    except Exception as e:
        logger.error(f"ID token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid ID token")
