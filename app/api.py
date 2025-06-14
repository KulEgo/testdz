from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
from redis.asyncio import Redis
import string
import random

app = FastAPI()

redis: Redis | None = None

class URLRequest(BaseModel):
    url: HttpUrl

def generate_short_id(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.on_event("startup")
async def startup_event():
    global redis
    redis = Redis.from_url("redis://localhost", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    if redis:
        await redis.close()

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    short_id = generate_short_id()
    # Проверяем на коллизии
    while await redis.exists(short_id):
        short_id = generate_short_id()
    await redis.set(short_id, request.url)
    return {"short_url": f"http://localhost:8000/{short_id}"}

@app.get("/{short_id}")
async def redirect_to_url(short_id: str):
    url = await redis.get(short_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url)

@app.get("/")
async def root():
    return {"message": "URL Shortener is running"}
