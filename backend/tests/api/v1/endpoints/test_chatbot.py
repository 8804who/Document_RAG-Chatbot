from unittest.mock import patch, MagicMock

import pytest


@pytest.mark.asyncio
async def test_chatbot_chat_success(authenticated_client):
    """Test chatbot chat endpoint with valid request"""
    with (
        patch("util.session_id.session_id_management", return_value="test_session_id"),
        patch("services.chat_service.get_answer") as mock_get_answer,
        patch("util.chatbot.save_chat_log") as mock_save_log,
    ):
        mock_response = MagicMock()
        mock_response.content = "This is a test response"
        mock_get_answer.return_value = mock_response

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
        patch("util.session_id.session_id_management", return_value="test_session_id"),
        patch(
            "services.chat_service.get_answer", side_effect=Exception("Service error")
        ),
    ):
        response = await authenticated_client.post(
            "/api/v1/chatbot/chat",
            json={"message": "Hello, chatbot!"},
            headers={"Authorization": "Bearer valid_token"},
        )

        assert response.status_code == 500
