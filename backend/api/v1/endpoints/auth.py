from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse
from core import config
from starlette.responses import RedirectResponse, JSONResponse
import logging
import requests
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from google.auth import jwt
import json


auth_router = APIRouter()
security = HTTPBearer()

BASE_URL = config.BASE_URL
GOOGLE_CLIENT_ID = config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = config.GOOGLE_CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


async def verify_google_token(token: str) -> dict:
    """
    Google에서 발급받은 access_token 인증

    Args:
        token (str): 인증받을 토큰

    Returns:
        dict: 토큰 정보
    """
    try:
        response = requests.get(
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

    except requests.RequestException as e:
        logging.error(f"Token verification failed: {e}")
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
        logging.error(f"ID token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid ID token")


@auth_router.get("/login")
async def login(request: Request):
    redirect_uri = f"{BASE_URL}/api/v1/auth/login/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)


@auth_router.get("/login/callback")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    token_verification = await verify_google_token(token["access_token"])

    userinfo_json = token.get("userinfo", {})
    userinfo_str = json.dumps(userinfo_json)

    if token["refresh_token"]:
        refresh_token = token["refresh_token"]
    else:
        refresh_token = None

    print(f"refresh_token: {refresh_token}")

    html_content = f"""
    <html>
      <body>
        <script>
          window.opener.postMessage(
            JSON.stringify({{
              access_token: "{token['access_token']}",
              id_token: "{token['id_token']}",
              userinfo: {userinfo_str},
              verified: {str(token_verification['valid']).lower()}
            }}), 
            "http://localhost:10002"
          );
          window.close();
        </script>
        <p>로그인 처리 중...</p>
      </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@auth_router.post("/verify")
async def verify_token_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    구글 Token 검증 엔드포인트

    Args:
        credentials (HTTPAuthorizationCredentials): 토큰

    Returns:
        dict: 토큰 정보
    """
    token = credentials.credentials

    try:
        verification_result = await verify_google_token(token)
        return verification_result
    except HTTPException:
        try:
            verification_result = await verify_google_id_token(token)
            return verification_result
        except HTTPException:
            raise HTTPException(status_code=401, detail="Invalid token")


@auth_router.post("/refresh")
async def refresh_token(request: Request) -> dict:
    """
    구글 Access Token 갱신

    Args:
        request (Request): 토큰 갱신 요청

    Returns:
        dict: 새롭게 발급 받은 토큰
    """
    try:
        body = await request.json()
        refresh_token = body.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token is required")

        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
            },
        )

        if response.status_code == 200:
            token_data = response.json()
            return {
                "access_token": token_data["access_token"],
                "expires_in": token_data.get("expires_in", 3600),
                "token_type": "Bearer",
            }
        else:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except Exception as e:
        logging.error(f"Token refresh failed: {e}")
        raise HTTPException(status_code=400, detail="Token refresh failed")


@auth_router.post("/logout")
async def logout(request: Request):
    """
    Revoke Google access token
    """
    try:
        body = await request.json()
        access_token = body.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Access token is required")

        response = requests.post(
            "https://oauth2.googleapis.com/revoke", data={"token": access_token}
        )

        if response.status_code == 200:
            return {"message": "Token revoked successfully"}
        else:
            return {"message": "Token revocation failed"}

    except Exception as e:
        logging.error(f"Token revocation failed: {e}")
        raise HTTPException(status_code=400, detail="Token revocation failed")
