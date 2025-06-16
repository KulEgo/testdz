from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from contextlib import asynccontextmanager

import models, schemas
from database import SessionLocal, engine

#старт тут
@asynccontextmanager
async def lifespan(_: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#основные методы
@app.post("/tasks/", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.TaskDB(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks/", response_model=List[schemas.TaskOut])
def get_tasks(
    sort_by: Optional[str] = Query(None, pattern="^(title|status|created_at)$"), search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.TaskDB)
    if search:
        query = query.filter((models.TaskDB.title.contains(search)) | (models.TaskDB.description.contains(search)))
    if sort_by:
        query = query.order_by(getattr(models.TaskDB, sort_by))
    return query.all()


@app.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, updated_task: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in updated_task.model_dump().items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskDB).filter_by(id=task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


@app.get("/tasks/top/{n}", response_model=List[schemas.TaskOut])
def get_top_priority_tasks(n: int, db: Session = Depends(get_db)):
    return db.query(models.TaskDB).order_by(models.TaskDB.priority.desc()).limit(n).all()
