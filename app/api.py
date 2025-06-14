from fastapi import FastAPI, HTTPException
from redis.asyncio import Redis
from .core import generate_short_code
from .storage import store_url, retrieve_url

app = FastAPI()
redis = None

@app.on_event("startup")
async def startup_event():
    global redis
    redis = Redis.from_url("redis://localhost", decode_responses=True)

@app.on_event("shutdown")
async def shutdown_event():
    await redis.close()

@app.post("/api/shorten")
async def shorten_url(request: ShortenRequest):
    short_code = generate_short_code()
    await store_url(redis, short_code, request.target_url)
    return {"short_code": short_code}

@app.get("/{short_code}")
async def redirect_to_target(short_code: str):
    url = await retrieve_url(redis, short_code)
    if url:
        from fastapi.responses import RedirectResponse
        return RedirectResponse(url=url, status_code=307)
    raise HTTPException(status_code=404, detail="Short code not found")
