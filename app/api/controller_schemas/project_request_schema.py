from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreateRequest(BaseModel):
    name: str = Field(..., example="My Project")
    description: str = Field("", example="This is my project description")


class ProjectUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, example="Updated Project Name")
    description: Optional[str] = Field(
        None, example="Updated project description"
    )
