# ...existing code...
# core/config.py (بدون dotenv)
import os
from typing import Any


class Config:
    """Configuration class for ToDoList application."""

    DATABASE_URL: str
    MAX_PROJECTS: int
    MAX_PROJECT_NAME_LENGTH: int
    MAX_PROJECT_DESC_LENGTH: int
    MAX_TASKS_PER_PROJECT: int
    MAX_TASK_NAME_LENGTH: int
    MAX_TASK_DESC_LENGTH: int

    def __init__(self) -> None:
        # Database configuration (PostgreSQL)
        self.DATABASE_URL = os.environ.get(
            "DATABASE_URL",
            "postgresql://todo_user:todo_password@localhost:5432/todo_db"
        )
        
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


# Instantiate settings at module level
settings = Config()