import pytest
from httpx import AsyncClient
from app.api import app

@pytest.mark.asyncio
async def test_shorten_and_redirect():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создать короткую ссылку
        response = await client.post("/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        data = response.json()
        assert "short_code" in data
        short_code = data["short_code"]

        # Проверить редирект
        response_redirect = await client.get(f"/{short_code}", follow_redirects=False)
        assert response_redirect.status_code == 307
        assert response_redirect.headers["location"] == "https://example.com"

@pytest.mark.asyncio
async def test_shorten_invalid_url():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/shorten", json={"url": "not a url"})
        assert response.status_code == 422  # или код валидации в вашем API

@pytest.mark.asyncio
async def test_redirect_404():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nonexistent")
        assert response.status_code == 404
