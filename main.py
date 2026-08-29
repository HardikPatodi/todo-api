from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
import sqlite3

from database import init_db, get_all_tasks, create_task, get_task_by_id, update_task, delete_task
from models import TaskCreate, TaskResponse, TaskUpdate

# --- App setup ---

app = FastAPI()

init_db()

# Enable CORS so a browser-based frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --- Endpoints ---

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks():
    """Retrieve all tasks, ordered newest first."""
    try:
        tasks = get_all_tasks()
        return tasks
    except sqlite3.Error as e:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def add_task(task: TaskCreate):
    """Create a new task. Returns 201 on success, 422 if validation fails, 503 if database unavailable."""
    try:
        task_id = create_task(task.title, task.description)
        return get_task_by_id(task_id)
    except sqlite3.Error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, task: TaskUpdate):
    """Update a task. Returns 200 on success, 404 if not found, 422 if validation fails, 503 if database unavailable."""
    try:
        updated = update_task(
            task_id,
            task.title,
            task.description,
            task.completed
        )
    
        if not updated:
            raise HTTPException(
                status_code=404,
                detail="Task not found"
            )
        return get_task_by_id(task_id)
    except sqlite3.Error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

@app.delete("/tasks/{task_id}", response_model=TaskResponse)
def remove_task(task_id: int):
    """Delete a task. Returns 200 on success, 404 if not found, 503 if database unavailable."""
    try:
        task = get_task_by_id(task_id)

        if task is None:
            raise HTTPException(
                status_code=404,
            detail="Task not found"
        )

        delete_task(task_id)

        return task
    except sqlite3.Error:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )