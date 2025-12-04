# core/services/validators.py

from typing import Optional
from core.config import Config
from core.models.task import Task


def validate_project_name(name: str, config: Config) -> None:
    if not name.strip():
        raise ValueError("Project name cannot be empty")

    if len(name) > config.MAX_PROJECT_NAME_LENGTH:
        raise ValueError(
            f"Project name cannot exceed {config.MAX_PROJECT_NAME_LENGTH} characters"
        )


def validate_project_description(description: str, config: Config) -> None:
    if len(description) > config.MAX_PROJECT_DESC_LENGTH:
        raise ValueError(
            f"Project description cannot exceed {config.MAX_PROJECT_DESC_LENGTH} characters"
        )


def validate_task_title(title: str, config: Config) -> None:
    if not title.strip():
        raise ValueError("Task title cannot be empty")

    if len(title) > config.MAX_TASK_NAME_LENGTH:
        raise ValueError(
            f"Task title cannot exceed {config.MAX_TASK_NAME_LENGTH} characters"
        )


def validate_task_description(description: str, config: Config) -> None:
    if len(description) > config.MAX_TASK_DESC_LENGTH:
        raise ValueError(
            f"Task description cannot exceed {config.MAX_TASK_DESC_LENGTH} characters"
        )


def validate_task_status(status: str) -> None:
    if status not in Task.VALID_STATUSES:
        valid = ", ".join(Task.VALID_STATUSES)
        raise ValueError(f"Invalid status. Valid statuses are: {valid}")
