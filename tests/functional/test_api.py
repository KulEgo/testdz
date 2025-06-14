import pytest
from httpx import AsyncClient
from app.api import app

@pytest.mark.asyncio
async def test_shorten_and_redirect():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Создаем короткую ссылку
        response = await client.post("/shorten", json={"url": "https://example.com"})
        assert response.status_code == 200
        data = response.json()
        short = data.get("short")
        assert short and isinstance(short, str)

        # Проверяем редирект по короткой ссылке
        response2 = await client.get(f"/{short}", follow_redirects=False)
        assert response2.status_code == 307
        assert response2.headers["location"] == "https://example.com"

@pytest.mark.asyncio
async def test_shorten_invalid_data():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/shorten", json={"wrong_field": "data"})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_redirect_404():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nonexistent")
        assert response.status_code == 404
