# app/api/controllers/project_controller.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from core.services.todo_manager import TodoManager
from app.api.dependencies import get_todo_manager
from app.api.controller_schemas.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
)
from app.api.controller_schemas.project_response_schema import (
    ProjectDetailResponse,
    ProjectListItemResponse,
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
)


@router.post(
    "/",
    response_model=ProjectDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    request: ProjectCreateRequest,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Create a new project."""
    try:
        project = manager.create_project(
            name=request.name,
            description=request.description,
        )
        return project
    except ValueError as e:
        # تبدیل خطاهای بیزینسی به HTTP 400
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=List[ProjectListItemResponse],
)
def list_projects(
    manager: TodoManager = Depends(get_todo_manager),
):
    """List all projects."""
    return manager.list_projects()


@router.get(
    "/{project_id}",
    response_model=ProjectDetailResponse,
)
def get_project(
    project_id: str,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Get a single project by ID."""
    project = manager.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )
    return project


@router.put(
    "/{project_id}",
    response_model=ProjectDetailResponse,
)
def update_project(
    project_id: str,
    request: ProjectUpdateRequest,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Update a project."""
    try:
        project = manager.edit_project(
            project_id=project_id,
            name=request.name,
            description=request.description,
        )
        return project
    except ValueError as e:
        msg = str(e)
        if "not found" in msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=msg,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: str,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Delete a project."""
    try:
        manager.delete_project(project_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    # 204 یعنی بدون body
    return None
