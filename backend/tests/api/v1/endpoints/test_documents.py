import pytest
from unittest.mock import patch


@pytest.mark.asyncio
async def test_documents_upload_success(client, mock_user):
    """Test document upload endpoint"""
    from app import app
    from util.dependencies import get_current_user

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        with patch("util.document.save_user_document_to_file") as mock_save, patch(
            "util.document.insert_document_to_vector_store"
        ) as mock_insert:

            file_content = "This is a test document"
            files = {"document": ("test.txt", file_content, "text/plain")}

            response = await client.post(
                "/api/v1/documents/user",
                files=files,
                headers={"Authorization": "Bearer valid_token"},
            )

            assert response.status_code == 200
            assert "message" in response.json()
            mock_save.assert_called_once()
            mock_insert.assert_called_once()
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_documents_upload_unauthenticated(client):
    """Test document upload endpoint without authentication"""
    files = {"document": ("test.txt", "content", "text/plain")}
    response = await client.post("/api/v1/documents/user", files=files)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_documents_get_success(client, mock_user):
    """Test get user documents endpoint"""
    from app import app
    from util.dependencies import get_current_user

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        with patch("util.document.get_user_documents_from_vector_store") as mock_get:

            mock_get.return_value = [
                {"id": "doc1", "name": "document1.txt"},
                {"id": "doc2", "name": "document2.txt"},
            ]

            response = await client.get(
                "/api/v1/documents/user",
                headers={"Authorization": "Bearer valid_token"},
            )

            assert response.status_code == 200
            assert "documents" in response.json()
            assert len(response.json()["documents"]) == 2
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_documents_get_unauthenticated(client):
    """Test get user documents endpoint without authentication"""
    response = await client.get("/api/v1/documents/user")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_documents_delete_success(client, mock_user):
    """Test delete document endpoint"""
    from app import app
    from util.dependencies import get_current_user

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    try:
        with patch("util.document.delete_document_from_vector_store") as mock_delete:

            document_id = "test-document-id"
            response = await client.delete(
                f"/api/v1/documents/{document_id}",
                headers={"Authorization": "Bearer valid_token"},
            )

            assert response.status_code == 200
            assert "message" in response.json()
            mock_delete.assert_called_once_with(document_id)
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_documents_delete_unauthenticated(client):
    """Test delete document endpoint without authentication"""
    response = await client.delete("/api/v1/documents/test-id")
    assert response.status_code == 403
