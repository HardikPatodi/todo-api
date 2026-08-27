import sqlite3
from datetime import datetime

DATABASE_PATH = "tasks.db"

def get_connection():
    """Return a SQLite connection with row_factory set for dict-like access."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the tasks table if it does not already exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                title        TEXT    NOT NULL,
                description  TEXT    DEFAULT '',
                completed    INTEGER NOT NULL DEFAULT 0,
                created_date TEXT    NOT NULL
            )
        """)


def get_all_tasks():
    """Retrieve every task from the database, ordered newest first."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks ORDER BY created_date DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_task_by_id(task_id: int):
    """Return a single task dict by ID, or None if it does not exist."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def create_task(title: str, description: str) -> int:
    """Insert a new task and return its auto-generated ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        created_date = datetime.now().isoformat()
        cursor.execute(
            "INSERT INTO tasks (title, description, completed, created_date) VALUES (?, ?, 0, ?)",
            (title, description, created_date),
        )
        return cursor.lastrowid


def update_task(task_id: int, title: str, description: str, completed: bool) -> bool:
    """Update an existing task's fields. Returns True if the row was found."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
            (title, description, int(completed), task_id),
        )
        return cursor.rowcount > 0


def delete_task(task_id: int) -> bool:
    """Delete a task by ID. Returns True if the row existed and was removed."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        return cursor.rowcount > 0