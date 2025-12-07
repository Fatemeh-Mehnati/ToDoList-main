# app/api/controllers/task_controller.py

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from core.services.todo_manager import TodoManager
from app.api.dependencies import get_todo_manager
from app.api.controller_schemas.task_request_schema import (
    TaskCreateRequest,
    TaskUpdateRequest,
)
from app.api.controller_schemas.task_response_schema import (
    TaskDetailResponse,
    TaskListItemResponse,
)

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.post(
    "/",
    response_model=TaskDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    request: TaskCreateRequest,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Create a new task."""
    try:
        task = manager.create_task(
            project_id=request.project_id,
            title=request.title,
            description=request.description,
            status=request.status,
            deadline=request.deadline,
        )
        return task
    except ValueError as e:
        msg = str(e)
        if "Project not found" in msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=msg,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


@router.get(
    "/",
    response_model=List[TaskListItemResponse],
)
def list_tasks(
    project_id: Optional[str] = None,
    manager: TodoManager = Depends(get_todo_manager),
):
    """
    List tasks.
    If project_id is provided, only tasks for that project are returned.
    """
    return manager.list_tasks(project_id=project_id)


@router.get(
    "/{task_id}",
    response_model=TaskDetailResponse,
)
def get_task(
    task_id: str,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Get a single task by ID."""
    task = manager.get_task(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    return task


@router.put(
    "/{task_id}",
    response_model=TaskDetailResponse,
)
def update_task(
    task_id: str,
    request: TaskUpdateRequest,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Update a task."""
    try:
        task = manager.edit_task(
            task_id=task_id,
            title=request.title,
            description=request.description,
            status=request.status,
            deadline=request.deadline,
        )
        return task
    except ValueError as e:
        msg = str(e)
        if "Task not found" in msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=msg,
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=msg,
        )


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    task_id: str,
    manager: TodoManager = Depends(get_todo_manager),
):
    """Delete a task."""
    try:
        manager.delete_task(task_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    return None


@router.post(
    "/close-overdue",
    summary="Close all overdue tasks",
)
def close_overdue_tasks(
    manager: TodoManager = Depends(get_todo_manager),
):
    """
    Close all tasks whose deadline has passed and are not done yet.
    Returns the number of tasks that were updated.
    """
    count = manager.close_overdue_tasks()
    return {"closed_tasks": count}
