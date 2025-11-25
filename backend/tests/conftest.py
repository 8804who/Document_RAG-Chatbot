from unittest.mock import patch

import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


# Shared test fixtures
@pytest.fixture
async def client():
    """Create a test client for the FastAPI app"""
    # Mock the lifespan dependencies to avoid initialization errors
    with (
        patch("app.util.chat_history.init_chat_history"),
        patch("app.util.chat_history.close_chat_history"),
        patch("app.util.logger.setup_logger"),
    ):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            yield ac


@pytest.fixture
def mock_user():
    """Mock user data for authentication"""
    return {
        "email": "test@example.com",
        "name": "Test User",
        "picture": "https://example.com/picture.jpg",
        "sub": "1234567890",
    }


async def authenticated_client(client, mock_user):
    """Create an authenticated test client"""
    from app.main import app
    from app.util.dependencies import get_current_user

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        yield client
    finally:
        app.dependency_overrides.clear()
