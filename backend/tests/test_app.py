import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    """Test the health check endpoint"""
    response = await client.get("/health")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "서버가 정상 실행중입니다" in response.json()["message"]
