import pytest
from unittest.mock import AsyncMock, patch, MagicMock


@pytest.mark.asyncio
async def test_auth_verify_token_success(client):
    """Test token verification endpoint with valid token"""
    with patch("api.v1.endpoints.auth.verify_google_token") as mock_verify:
        mock_verify.return_value = {
            "valid": True,
            "user_info": {
                "email": "test@example.com",
                "name": "Test User",
                "picture": "https://example.com/picture.jpg",
                "sub": "1234567890",
            },
        }

        response = await client.post(
            "/api/v1/auth/verify", headers={"Authorization": "Bearer valid_token"}
        )

        assert response.status_code == 200
        assert response.json()["valid"] is True
        assert "user_info" in response.json()


@pytest.mark.asyncio
async def test_auth_verify_token_invalid(client):
    """Test token verification endpoint with invalid token"""
    with patch("api.v1.endpoints.auth.verify_google_token") as mock_verify, patch(
        "api.v1.endpoints.auth.verify_google_id_token"
    ) as mock_verify_id:
        mock_verify.side_effect = Exception("Invalid token")
        mock_verify_id.side_effect = Exception("Invalid token")

        response = await client.post(
            "/api/v1/auth/verify", headers={"Authorization": "Bearer invalid_token"}
        )

        assert response.status_code == 401


@pytest.mark.asyncio
async def test_auth_verify_token_missing(client):
    """Test token verification endpoint without token"""
    response = await client.post("/api/v1/auth/verify")
    assert response.status_code == 403  # FastAPI returns 403 for missing credentials


@pytest.mark.asyncio
async def test_auth_refresh_token_success(client):
    """Test token refresh endpoint with valid refresh token"""
    with patch("api.v1.endpoints.auth.get_google_oauth_token") as mock_get_token, patch(
        "api.v1.endpoints.auth.httpx.AsyncClient"
    ) as mock_client_class:
        mock_get_token.return_value = "valid_refresh_token"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "new_access_token",
            "expires_in": 3600,
            "token_type": "Bearer",
        }

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = await client.post(
            "/api/v1/auth/refresh", json={"email": "test@example.com"}
        )

        assert response.status_code == 200
        assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_auth_refresh_token_missing_email(client):
    """Test token refresh endpoint without email"""
    response = await client.post("/api/v1/auth/refresh", json={})
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_auth_logout_success(client):
    """Test logout endpoint with valid token"""
    with patch("api.v1.endpoints.auth.httpx.AsyncClient") as mock_client_class:
        mock_response = MagicMock()
        mock_response.status_code = 200

        mock_client = AsyncMock()
        mock_client.post = AsyncMock(return_value=mock_response)
        mock_client_class.return_value.__aenter__.return_value = mock_client

        response = await client.post(
            "/api/v1/auth/logout", json={"access_token": "valid_token"}
        )

        assert response.status_code == 200
        assert "message" in response.json()


@pytest.mark.asyncio
async def test_auth_logout_missing_token(client):
    """Test logout endpoint without token"""
    response = await client.post("/api/v1/auth/logout", json={})
    assert response.status_code == 400
