from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from database import init_db, get_all_tasks, create_task, get_task_by_id, update_task
from models import TaskCreate, TaskResponse, TaskUpdate

# --- App setup ---

app = FastAPI()

init_db()

# Enable CORS so a browser-based frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
)
# --- Endpoints ---

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks():
    """Retrieve all tasks, ordered newest first."""
    tasks = get_all_tasks()
    return tasks

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def add_task(task: TaskCreate):
    task_id = create_task(
        task.title,
        task.description
    )

    return get_task_by_id(task_id)

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def edit_task(task_id: int, task: TaskUpdate):

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