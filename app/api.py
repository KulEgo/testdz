from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import redis.asyncio as redis
from app.core import generate_short_code
from app.storage import store_url, retrieve_url

app = FastAPI()

redis_client = redis.from_url("redis://localhost", decode_responses=True)

class URLRequest(BaseModel):
    target_url: str

@app.post("/api/shorten")
async def create_short_url(data: URLRequest):
    short_code = generate_short_code()
    await store_url(redis_client, short_code, data.target_url)
    return {"short_code": short_code}

@app.get("/{short_code}")
async def redirect(short_code: str, request: Request):
    url = await retrieve_url(redis_client, short_code)
    if url:
        return RedirectResponse(url, status_code=307)
    raise HTTPException(status_code=404, detail="URL not found")

