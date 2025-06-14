async def store_url(redis, short_code: str, target_url: str):
    await redis.set(short_code, target_url)

async def retrieve_url(redis, short_code: str):
    result = await redis.get(short_code)
    if result:
        return result.decode("utf-8")
    return None