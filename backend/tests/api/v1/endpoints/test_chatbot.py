from unittest.mock import AsyncMock, patch

import pytest
from langchain_core.messages import BaseMessage

from app.main import app


@pytest.mark.asyncio
async def test_chatbot_chat_success(authenticated_client):
    """Test the chatbot chat endpoint with a valid request."""
    with (
        patch(
            "app.api.v1.endpoints.chatbot.session_id_management",
            new_callable=AsyncMock,
        ) as mock_session_id_management,
        patch(
            "app.api.v1.endpoints.chatbot.save_chat_log",
            new_callable=AsyncMock,
        ) as mock_save_log,
        patch.object(
            app.state.chat_service,
            "get_answer",
            new_callable=AsyncMock,
        ) as mock_get_answer,
    ):
        mock_session_id_management.return_value = "test_session_id"
        mock_save_log.return_value = None
        mock_get_answer.return_value = BaseMessage(
            type="ai", content="This is a test response"
        )

        response = await authenticated_client.post(
            "/api/v1/chatbot/chat",
            json={"message": "Hello, chatbot!"},
        )

        assert response.status_code == 200
        assert response.json() == {"answer": "This is a test response"}

        mock_session_id_management.assert_awaited_once()
        mock_get_answer.assert_awaited_once()
        mock_save_log.assert_awaited_once()


@pytest.mark.asyncio
async def test_chatbot_chat_unauthenticated(client):
    """Test chatbot chat endpoint without authentication"""
    response = await client.post(
        "/api/v1/chatbot/chat", json={"message": "Hello, chatbot!"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_chatbot_chat_missing_message(authenticated_client):
    """Test chatbot chat endpoint without message"""
    response = await authenticated_client.post(
        "/api/v1/chatbot/chat",
        json={},
        headers={"Authorization": "Bearer valid_token"},
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_chatbot_chat_error_handling(authenticated_client):
    """Test chatbot chat endpoint error handling"""
    from app.main import app

    with (
        patch(
            "app.api.v1.endpoints.chatbot.session_id_management",
            new_callable=AsyncMock,
        ) as mock_session_id_management,
    ):
        mock_session_id_management.return_value = "test_session_id"

        # Mock the chat_service.get_answer method to raise an exception
        app.state.chat_service.get_answer = AsyncMock(
            side_effect=Exception("Service error")
        )

        response = await authenticated_client.post(
            "/api/v1/chatbot/chat",
            json={"message": "Hello, chatbot!"},
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 500
