import json
import httpx

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import HTMLResponse, JSONResponse

from app.core.config import settings
from app.util.auth import (
    save_google_oauth_token,
    get_google_oauth_token,
    verify_google_token,
    verify_google_id_token,
)
from app.util.logger import logger

auth_router = APIRouter()
security = HTTPBearer()

BASE_URL = settings.BASE_URL
GOOGLE_CLIENT_ID = settings.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET.get_secret_value(),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@auth_router.get("/login")
async def login(request: Request):
    redirect_uri = f"{BASE_URL}/api/v1/auth/login/callback"
    return await oauth.google.authorize_redirect(
        request, redirect_uri, access_type="offline", prompt="consent"
    )


@auth_router.get("/login/callback")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    token_verification = await verify_google_token(token["access_token"])

    userinfo_json = token.get("userinfo", {})
    userinfo_str = json.dumps(userinfo_json)

    refresh_token = token["refresh_token"]
    if refresh_token:
        await save_google_oauth_token(
            name=userinfo_json.get("name"),
            email=userinfo_json.get("email"),
            refresh_token=refresh_token,
        )

    html_content = f"""
    <html>
      <body>
        <script>
          window.opener.postMessage(
            JSON.stringify({{
              access_token: "{token["access_token"]}",
              id_token: "{token["id_token"]}",
              userinfo: {userinfo_str},
              verified: {str(token_verification["valid"]).lower()}
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
) -> JSONResponse:
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
        return JSONResponse(content=verification_result, status_code=200)
    except HTTPException:
        try:
            verification_result = await verify_google_id_token(token)
            return JSONResponse(content=verification_result, status_code=200)
        except HTTPException:
            raise HTTPException(status_code=401, detail="Invalid token")


@auth_router.post("/refresh")
async def refresh_token(request: Request) -> JSONResponse:
    """
    구글 Access Token 갱신

    Args:
        request (Request): 토큰 갱신 요청

    Returns:
        dict: 새롭게 발급 받은 토큰
    """
    try:
        body = await request.json()
        refresh_token = await get_google_oauth_token(body.get("email"))

        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token is required")

        async with httpx.AsyncClient() as client:
            response = await client.post(
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
            return JSONResponse(
                content={
                    "access_token": token_data["access_token"],
                    "expires_in": token_data.get("expires_in", 3600),
                    "token_type": "Bearer",
                },
                status_code=200,
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/revoke", data={"token": access_token}
            )

        if response.status_code == 200:
            return JSONResponse(
                content={"message": "Token revoked successfully"}, status_code=200
            )
        else:
            return JSONResponse(
                content={"message": "Token revocation failed"}, status_code=400
            )

    except Exception as e:
        logger.error(f"Token revocation failed: {e}")
        raise HTTPException(status_code=400, detail="Token revocation failed")
