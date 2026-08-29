from pydantic import BaseModel, Field, field_validator

class TaskCreate(BaseModel):
    """Schema for creating a new task (POST request body)."""
    title: str = Field(..., min_length=1, description="Task title (required, non-empty)")
    description: str = Field(
        default="",
        description="Task description (optional)"
    )
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_whitespace(cls, v):
        if not v or v.strip() == '':
            raise ValueError('title cannot be empty or whitespace only')
        return v.strip()


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (PUT request body)."""
    title: str = Field(..., min_length=1, description="Updated title")
    description: str = Field(
        default="",
        description="Updated description (optional)"
    )
    completed: bool = Field(default=False, description="Whether the task is complete")
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_whitespace(cls, v):
        if not v or v.strip() == '':
            raise ValueError('title cannot be empty or whitespace only')
        return v.strip()


class TaskResponse(BaseModel):
    """Schema for task responses (GET, POST, PUT responses)."""
    id: int
    title: str
    description: str
    completed: bool
    created_date: str

    class Config:
        from_attributes = True