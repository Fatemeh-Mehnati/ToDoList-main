# ...existing code...
# core/config.py (بدون dotenv)
import os
from typing import Any


class Config:
    """Configuration class for ToDoList application."""

    MAX_PROJECTS: int
    MAX_PROJECT_NAME_LENGTH: int
    MAX_PROJECT_DESC_LENGTH: int
    MAX_TASKS_PER_PROJECT: int
    MAX_TASK_NAME_LENGTH: int
    MAX_TASK_DESC_LENGTH: int

    def __init__(self) -> None:
        # Project limits (with default values)
        self.MAX_PROJECTS = int(os.environ.get("MAX_PROJECTS", "10"))
        self.MAX_PROJECT_NAME_LENGTH = int(
            os.environ.get("MAX_PROJECT_NAME_LENGTH", "30")
        )
        self.MAX_PROJECT_DESC_LENGTH = int(
            os.environ.get("MAX_PROJECT_DESC_LENGTH", "150")
        )

        # Task limits
        self.MAX_TASKS_PER_PROJECT = int(
            os.environ.get("MAX_TASKS_PER_PROJECT", "20")
        )
        self.MAX_TASK_NAME_LENGTH = int(
            os.environ.get("MAX_TASK_NAME_LENGTH", "30")
        )
        self.MAX_TASK_DESC_LENGTH = int(
            os.environ.get("MAX_TASK_DESC_LENGTH", "150")
        )

    def __repr__(self) -> str:
        return (
            f"Config(MAX_PROJECTS={self.MAX_PROJECTS}, "
            f"MAX_TASKS_PER_PROJECT={self.MAX_TASKS_PER_PROJECT})"
        )
# ...existing code...