from fastapi import FastAPI, HTTPException, status
import redis.asyncio as redis

app = FastAPI()

redis_client: redis.Redis | None = None

@app.on_event("startup")
async def startup_event():
    global redis_client
    # Подключение к Redis (пример с локальным сервером)
    redis_client = redis.from_url("redis://localhost", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    if redis_client:
        await redis_client.close()

@app.post("/api/shorten")
async def create_short_url(target_url: str):
    if not redis_client:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Redis not connected")

    # пример генерации кода
    short_code = "abc123"
    await redis_client.set(short_code, target_url)
    return {"short_code": short_code}

@app.get("/{short_code}")
async def redirect(short_code: str):
    if not redis_client:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Redis not connected")

    target_url = await redis_client.get(short_code)
    if target_url is None:
        raise HTTPException(status_code=404, detail="Short code not found")

    return {"location": target_url}
