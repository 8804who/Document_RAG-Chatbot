import sys
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient, ASGITransport

# Add the backend directory (parent of tests) to the Python path
backend_dir = Path(__file__).parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app import app


# Shared test fixtures
@pytest.fixture
async def client():
    """Create a test client for the FastAPI app"""
    # Mock the lifespan dependencies to avoid initialization errors
    with patch("util.chat_history.init_chat_history"), patch(
        "util.chat_history.close_chat_history"
    ), patch("util.logger.setup_logger"):
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
