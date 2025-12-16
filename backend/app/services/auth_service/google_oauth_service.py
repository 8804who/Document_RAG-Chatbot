import httpx
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

from app.core.config import settings
from app.crud import auth as auth_crud
from app.db.database import get_async_db_session
from app.services.auth_service.auth_service import AuthService
from app.util.logger import logger


class GoogleOauthService(AuthService):
    def __init__(self):
        self.google_client_id = settings.GOOGLE_CLIENT_ID
        self.google_client_secret = settings.GOOGLE_CLIENT_SECRET

    async def verify_token(self, token: str) -> bool:
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
                    f"https://oauth2.googleapis.com/tokeninfo?access_token={token}",
                    timeout=10,
                )

            if response.status_code == 200:
                token_info = response.json()

                if token_info.get("aud") != self.google_client_id:
                    raise Exception("Invalid token audience")

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
                raise Exception("Invalid token")

        except httpx.RequestException as e:
            logger.error(f"Token verification failed: {e}")
            raise Exception("Token verification failed")


    async def verify_id_token(self, id_token_str: str) -> bool:
        """
        Google ID Token 인증

        Args:
            id_token_str (str):

        Returns:
            dict: 토큰 정보

        """
        try:
            idinfo = id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), self.google_client_id
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
            raise Exception("Invalid ID token")


    async def save_token(self, name: str, email: str, refresh_token: str) -> bool:
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


    async def get_token(self, email: str) -> str:
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
