import pytest
from app.storage import Storage

@pytest.fixture
def storage():
    return Storage()

def test_storage_save_and_get(storage):
    key = "abc123"
    url = "https://example.com"
    storage.save(key, url)
    assert storage.get(key) == url

def test_storage_get_nonexistent(storage):
    assert storage.get("nonexistent") is None
    
