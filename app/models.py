from pydantic import BaseModel

class URLIn(BaseModel):
    url: str

class URLOut(BaseModel):
    short_code: str

class URLRedirect(BaseModel):
    url: str
