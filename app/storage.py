class Storage:
    def __init__(self, redis):
        self.redis = redis

    async def store_url(self, short_code: str, target_url: str):
        await self.redis.set(short_code, target_url)

    async def retrieve_url(self, short_code: str):
        result = await self.redis.get(short_code)
        if result:
            return result.decode("utf-8")
        return None
