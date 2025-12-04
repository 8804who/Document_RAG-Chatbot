from unittest.mock import patch, AsyncMock

from langchain_core.messages import BaseMessage
import pytest


@pytest.mark.asyncio
async def test_chatbot_chat_success(authenticated_client):
    """Test chatbot chat endpoint with valid request"""
    with (
        patch(
            "app.api.v1.endpoints.chatbot.session_id_management",
            new_callable=AsyncMock,
        ) as mock_session_id_management,
        patch(
            "app.api.v1.endpoints.chatbot.get_answer",
            new_callable=AsyncMock,
        ) as mock_get_answer,
        patch(
            "app.api.v1.endpoints.chatbot.save_chat_log",
            new_callable=AsyncMock,
        ) as mock_save_log,
    ):
        mock_session_id_management.return_value = "test_session_id"
        mock_get_answer.return_value = BaseMessage(
            type="ai", content="This is a test response"
        )
        mock_save_log.return_value = None

        response = await authenticated_client.post(
            "/api/v1/chatbot/chat",
            json={"message": "Hello, chatbot!"},
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 200
        assert "answer" in response.json()
        assert response.json()["answer"] == "This is a test response"


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
    with (
        patch(
            "app.api.v1.endpoints.chatbot.session_id_management",
            new_callable=AsyncMock,
        ) as mock_session_id_management,
        patch(
            "app.api.v1.endpoints.chatbot.get_answer",
            new_callable=AsyncMock,
        ),
    ):
        mock_session_id_management.return_value = "test_session_id"
        # Configure the async mock to raise an exception when awaited
        mock_session_id_management.side_effect = None
        patch_target = "app.api.v1.endpoints.chatbot.get_answer"
        with patch(patch_target, new_callable=AsyncMock) as failing_get_answer:
            failing_get_answer.side_effect = Exception("Service error")

        response = await authenticated_client.post(
            "/api/v1/chatbot/chat",
            json={"message": "Hello, chatbot!"},
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 500
