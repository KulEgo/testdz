from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
import redis.asyncio as redis
from contextlib import asynccontextmanager

# Инициализируем redis клиент глобально, чтобы использовать в приложении
redis_client = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = redis.from_url("redis://localhost", decode_responses=True)
    yield
    await redis_client.close()

app = FastAPI(lifespan=lifespan)

class Link(BaseModel):
    url: HttpUrl

async def generate_short_key() -> str:
    # Пример простой генерации, можно улучшить
    import secrets, string
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(6))

@app.post("/shorten")
async def shorten(link: Link):
    key = await generate_short_key()
    await redis_client.set(key, link.url)
    return {"short_url": f"http://localhost:8000/{key}"}

@app.get("/{key}")
async def redirect_to_url(key: str):
    url = await redis_client.get(key)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url)

@app.get("/")
async def root():
    return {"message": "URL Shortener is running."}
