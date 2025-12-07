from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ProjectBaseResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class ProjectListItemResponse(ProjectBaseResponse):
    """Single project item for list endpoints."""
    pass


class ProjectDetailResponse(ProjectBaseResponse):
    """Detailed project response (later می‌تونیم لیست تسک‌ها رو هم بهش اضافه کنیم)."""
    # later: tasks: List["TaskListItemResponse"] = []
    pass
