from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, get_all_tasks
from models import TaskResponse

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
