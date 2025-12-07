from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    project_id: str = Field(..., example="project-uuid")
    title: str = Field(..., example="Buy milk")
    description: str = Field("", example="Buy 2L milk from the store.")
    status: str = Field("todo", example="todo")
    deadline: Optional[datetime] = Field(
        None, example="2025-12-31T23:59:00"
    )


class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None, example="Updated task title")
    description: Optional[str] = Field(
        None, example="Updated task description"
    )
    status: Optional[str] = Field(None, example="in_progress")
    deadline: Optional[datetime] = Field(
        None, example="2025-12-31T23:59:00"
    )
