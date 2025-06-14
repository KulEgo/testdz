import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch
from app.api import app

@pytest.mark.asyncio
async def test_create_and_redirect():
    mock_store = AsyncMock()
    mock_retrieve = AsyncMock(return_value="https://google.com")

    with patch("app.api.store_url", mock_store), patch("app.api.retrieve_url", mock_retrieve):
        with patch("app.api.redis", AsyncMock()):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.post("/api/shorten", json={"target_url": "https://google.com"})
                assert response.status_code == 200
                data = response.json()
                assert "short_code" in data

                redirect = await ac.get(f"/{data['short_code']}", follow_redirects=False)
                assert redirect.status_code == 307
                assert redirect.headers["location"] == "https://google.com"

@pytest.mark.asyncio
async def test_shorten_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_redirect_404():
    with patch("app.api.retrieve_url", new_callable=AsyncMock) as mock_retrieve:
        mock_retrieve.return_value = None
        with patch("app.api.redis", AsyncMock()):
            async with AsyncClient(app=app, base_url="http://test") as ac:
                response = await ac.get("/nonexistent", follow_redirects=False)
                assert response.status_code == 404
                assert response.json() == {"detail": "Short code not found"}

