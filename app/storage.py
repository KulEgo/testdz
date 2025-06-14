async def store_url(redis_client, short_code: str, target_url: str):
    await redis_client.set(short_code, target_url)

async def retrieve_url(redis_client, short_code: str):
    result = await redis_client.get(short_code)
    if result:
        return result  # Уже строка
    return None
