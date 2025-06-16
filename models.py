from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pending")
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
