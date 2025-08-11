from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from api.v1.endpoints.auth import verify_google_token, verify_google_id_token
import logging

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """
    토큰 검증 후 현재 사용자 정보 반환

    Args:
        credentials: HTTP Bearer 토큰 정보

    Returns:
        dict: 인증된 사용자 정보

    Raises:
        HTTPException: 토큰이 유효하지 않거나 인증 실패 시 예외 발생
    """
    try:
        token = credentials.credentials

        try:
            user_info = await verify_google_token(token)
            return user_info["user_info"]
        except HTTPException:
            try:
                user_info = await verify_google_id_token(token)
                return user_info["user_info"]
            except HTTPException:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication token",
                    headers={"WWW-Authenticate": "Bearer"},
                )

    except Exception as e:
        logging.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict | None:
    """
    선택적 인증 - 토큰이 유효하면 사용자 정보 반환, 그렇지 않으면 None 반환
    인증 여부에 따라 작동하는 엔드포인트에 유용

    Args:
        credentials: HTTP Bearer 토큰 정보

    Returns:
        dict or None: 인증된 사용자 정보 또는 None
    """
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
