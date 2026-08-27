from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    """Schema for creating a new task (POST request body)."""
    title: str = Field(..., min_length=1, description="Task title (required, non-empty)")
    description: str = Field(
        default="",
        description="Task description (optional)"
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (PUT request body)."""
    title: str = Field(..., min_length=1, description="Updated title")
    description: str = Field(
        default="",
        description="Updated description (optional)"
    )
    completed: bool = Field(default=False, description="Whether the task is complete")


class TaskResponse(BaseModel):
    """Schema for task responses (GET, POST, PUT responses)."""
    id: int
    title: str
    description: str
    completed: bool
    created_date: str

    class Config:
        from_attributes = True