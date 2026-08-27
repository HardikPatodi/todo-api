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
    conn = get_connection()
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
    conn.commit()
    conn.close()


def get_all_tasks():
    """Retrieve every task from the database, ordered newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks ORDER BY created_date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_task_by_id(task_id: int):
    """Return a single task dict by ID, or None if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def create_task(title: str, description: str) -> int:
    """Insert a new task and return its auto-generated ID."""
    conn = get_connection()
    cursor = conn.cursor()
    created_date = datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO tasks (title, description, completed, created_date) VALUES (?, ?, 0, ?)",
        (title, description, created_date),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def update_task(task_id: int, title: str, description: str, completed: bool) -> bool:
    """Update an existing task's fields. Returns True if the row was found."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?",
        (title, description, int(completed), task_id),
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_task(task_id: int) -> bool:
    """Delete a task by ID. Returns True if the row existed and was removed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted
