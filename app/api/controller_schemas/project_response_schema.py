from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ProjectBaseResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime

    # Pydantic v2 config – جایگزین orm_mode
    model_config = {"from_attributes": True}


class ProjectListItemResponse(ProjectBaseResponse):
    """Single project item for list endpoints."""
    pass


class ProjectDetailResponse(ProjectBaseResponse):
    """Detailed project response."""
    pass
