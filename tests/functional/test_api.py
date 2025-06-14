import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.api import app


@pytest.mark.asyncio
async def test_create_and_redirect():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={"target_url": "https://google.com"})
        assert response.status_code == 200
        data = response.json()
        assert "short_code" in data

        redirect = await ac.get(f"/{data['short_code']}", follow_redirects=False)
        assert redirect.status_code == 307
        assert redirect.headers["location"] == "https://google.com"


@pytest.mark.asyncio
async def test_shorten_invalid_data():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/shorten", json={})
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_redirect_404():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/nonexistent123", follow_redirects=False)
        assert response.status_code == 404


