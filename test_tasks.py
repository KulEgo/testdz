import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
#Тут вставил таким образом, потому что командная строка при запуске тестов ну ни в какую не хотела видель src

import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy import inspect
import models



client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_lifespan_creates_tables():
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "tasks" in tables

def test_get_db_yields_session():
    gen = get_db()
    db_session = next(gen)
    assert isinstance(db_session, Session)
    try:
        next(gen)
    except StopIteration:
        pass

def test_create_task(db):
    response = client.post("/tasks/", json={
        "title": "Test task",
        "description": "Test description",
        "status": "pending",
        "priority": 1
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test task"
    assert "id" in data

def test_get_tasks_sort_and_search(db):
    client.post("/tasks/", json={"title": "abc", "description": "desc", "status": "pending"})
    client.post("/tasks/", json={"title": "def", "description": "desc2", "status": "done"})
    response = client.get("/tasks/", params={"search": "abc"})
    assert response.status_code == 200
    tasks = response.json()
    assert all("abc" in task["title"] for task in tasks)

    response = client.get("/tasks/", params={"sort_by": "status"})
    assert response.status_code == 200
    tasks = response.json()
    statuses = [task["status"] for task in tasks]
    assert statuses == sorted(statuses)

def test_get_task_not_found():
    response = client.get("/tasks/9999")
    assert response.status_code == 404

def test_update_task(db):
    response = client.post("/tasks/", json={
        "title": "Update test",
        "description": "desc",
        "status": "pending"
    })
    task_id = response.json()["id"]
    response = client.put(f"/tasks/{task_id}", json={
        "title": "Updated title",
        "description": "desc",
        "status": "done"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["status"] == "done"

def test_delete_task(db):
    response = client.post("/tasks/", json={
        "title": "Delete test",
        "description": "desc",
        "status": "pending"
    })
    task_id = response.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404

def test_get_top_priority_tasks(db):
    client.post("/tasks/", json={"title": "Low", "description": "desc", "status": "pending", "priority": 1})
    client.post("/tasks/", json={"title": "High", "description": "desc", "status": "pending", "priority": 10})
    response = client.get("/tasks/top/1")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["priority"] == 10

def test_get_tasks_complex_logic(db):
    db_task1 = models.TaskDB(title="Buy milk", description="", status="pending", priority=1)
    db_task2 = models.TaskDB(title="Fix bug", description="bug", status="done", priority=3)
    db.add_all([db_task1, db_task2])
    db.commit()
    
    response = client.get("/tasks/", params={"search": "bug"})
    assert response.status_code == 200
    assert any(task["title"] == "Fix bug" for task in response.json())

def test_get_task_mocked(mocker):
    mock_db = mocker.MagicMock()
    mock_task = models.TaskDB(
        id=1,
        title="Mocked",
        description="Test description",
        status="pending",
        priority=0
    )
    mock_db.query.return_value.filter_by.return_value.first.return_value = mock_task
    mocker.patch("main.get_db", return_value=iter([mock_db]))
    
    response = client.get("/tasks/1")
    assert response.status_code == 200
    assert response.json()["description"] == "Test description"  # Проверяем реальное значение

def test_create_task_invalid_data():
    response = client.post("/tasks/", json={"title": "Valid", "status": "pending"})
    assert response.status_code == 422
    
    response = client.post("/tasks/", json={"title": "", "status": "pending"})
    assert response.status_code == 422

    response = client.post("/tasks/", json={"title": "Valid", "status": "invalid_status"})
    assert response.status_code == 422

def test_get_tasks_sort_by_created_at(db):
    db.query(models.TaskDB).delete()
    db.commit()
    
    db_task1 = models.TaskDB(title="Task1", description="desc1", status="pending")
    db_task2 = models.TaskDB(title="Task2", description="desc2", status="done")
    db.add_all([db_task1, db_task2])
    db.commit()

    response = client.get("/tasks/", params={"sort_by": "created_at"})
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["created_at"] <= tasks[1]["created_at"]

def test_create_task_default_priority(db):
    response = client.post("/tasks/", json={
        "title": "No priority",
        "description": "test",
        "status": "pending"
    })
    assert response.json()["priority"] == 0
