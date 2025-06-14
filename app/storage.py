storage = {}

async def store_url(short_code: str, url: str):
    storage[short_code] = url

async def retrieve_url(short_code: str) -> str | None:
    return storage.get(short_code)
