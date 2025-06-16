from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    priority: Optional[int] = 0  # Теперь необязательное поле

class TaskOut(TaskCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
