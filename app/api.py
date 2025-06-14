from fastapi import FastAPI, HTTPException
from app.core import generate_short_code
from app.storage import store_url, retrieve_url
from pydantic import BaseModel

app = FastAPI()

class URLIn(BaseModel):
    url: str

@app.post("/shorten")
async def shorten_url(data: URLIn):
    short_code = generate_short_code(data.url)
    await store_url(short_code, data.url)
    return {"short_code": short_code}

@app.get("/{short_code}")
async def redirect(short_code: str):
    url = await retrieve_url(short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"url": url}

