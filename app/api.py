from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import redis.asyncio as redis 

app = FastAPI()
redis_client = redis.from_url("redis://localhost", decode_responses=True)

class ShortenRequest(BaseModel):
    url: str

@app.on_event("startup")
async def startup_event():
    global redis_client
    redis_client = redis.from_url("redis://localhost", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    global redis_client
    if redis_client:
        await redis_client.close()

# Пример эндпоинта сокращения URL
@app.post("/shorten")
async def shorten_url(data: ShortenRequest):
    # Пример генерации кода (здесь нужно свою логику)
    short_code = "abc123"  # заглушка, сделай свою генерацию уникального кода

    # Сохраняем в Redis: short_code -> url
    await redis_client.set(short_code, data.url)

    return {"short_code": short_code, "url": data.url}

# Эндпоинт перенаправления
@app.get("/{short_code}")
async def redirect_short_url(short_code: str):
    url = await redis_client.get(short_code)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url)


