from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBaseResponse(BaseModel):
    id: str
    project_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    deadline: Optional[datetime] = None

    class Config:
        orm_mode = True


class TaskListItemResponse(TaskBaseResponse):
    """Single task item for list endpoints."""
    pass


class TaskDetailResponse(TaskBaseResponse):
    """Detailed task response."""
    pass
