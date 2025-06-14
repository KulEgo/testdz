import pytest
from unittest.mock import AsyncMock
from app.storage import store_url, retrieve_url

@pytest.mark.asyncio
async def test_store_and_retrieve_url():
    fake_redis = AsyncMock()
    fake_redis.get.return_value = b"https://example.com"

    await store_url(fake_redis, "abc123", "https://example.com")
    result = await retrieve_url(fake_redis, "abc123")
    assert result == "https://example.com"
