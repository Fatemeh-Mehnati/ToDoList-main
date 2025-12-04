# core/services/todo_manager.py (or core/todo_manager.py)

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core.models.project import Project
from core.models.task import Task
from core.config import Config
from core.repositories.project_repository import ProjectRepository
from core.repositories.task_repository import TaskRepository


class TodoManager:
    """Manage projects and tasks using repositories and SQLAlchemy."""

    def __init__(self, db: Session, config: Optional[Config] = None) -> None:
        self.db = db
        self.config = config if config else Config()

        # Repositories
        self.projects = ProjectRepository(db)
        self.tasks = TaskRepository(db)

    # ==================== Project Management ====================

    def create_project(self, name: str, description: str) -> Project:
        """Create a new project with validation."""

        # Check project count limit
        project_count = self.projects.count()
        if project_count >= self.config.MAX_PROJECTS:
            raise ValueError(
                f"Cannot create more than {self.config.MAX_PROJECTS} projects"
            )

        # Check name + description length
        if len(name) > self.config.MAX_PROJECT_NAME_LENGTH:
            raise ValueError(
                f"Project name cannot exceed {self.config.MAX_PROJECT_NAME_LENGTH} characters"
            )

        if len(description) > self.config.MAX_PROJECT_DESC_LENGTH:
            raise ValueError(
                f"Project description cannot exceed {self.config.MAX_PROJECT_DESC_LENGTH} characters"
            )

        # Duplicate name check
        if self.projects.get_by_name(name):
            raise ValueError(f"Project with name '{name}' already exists")

        # Delegate creation to repository
        return self.projects.create(name=name, description=description)

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def list_projects(self) -> List[Project]:
        return self.projects.list()

    def edit_project(
        self,
        project_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")

        # Validate fields
        if name:
            if len(name) > self.config.MAX_PROJECT_NAME_LENGTH:
                raise ValueError("Project name too long")

            # Check for duplicate name (excluding this project)
            existing = (
                self.db.query(Project)
                .filter(Project.name == name, Project.id != project_id)
                .first()
            )
            if existing:
                raise ValueError(f"Project with name '{name}' already exists")

            project.name = name

        if description:
            if len(description) > self.config.MAX_PROJECT_DESC_LENGTH:
                raise ValueError("Description too long")
            project.description = description

        self.db.commit()
        self.db.refresh(project)
        return project

    def delete_project(self, project_id: str) -> bool:
        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")

        # Cascade deletes tasks automatically (as defined in model relationship)
        self.projects.delete(project)
        return True

    # ==================== Task Management ====================

    def create_task(
        self,
        project_id: str,
        title: str,
        description: str,
        status: str = "todo",
        deadline: Optional[datetime] = None,
    ) -> Task:
        """Create a new task under a project with validation."""

        project = self.get_project(project_id)
        if not project:
            raise ValueError("Project not found")

        # Task count constraint
        task_count = self.tasks.count_by_project(project_id)
        if task_count >= self.config.MAX_TASKS_PER_PROJECT:
            raise ValueError(
                f"Cannot create more than {self.config.MAX_TASKS_PER_PROJECT} tasks for this project"
            )

        if len(title) > self.config.MAX_TASK_NAME_LENGTH:
            raise ValueError("Task title too long")

        if len(description) > self.config.MAX_TASK_DESC_LENGTH:
            raise ValueError("Task description too long")

        if status not in Task.VALID_STATUSES:
            raise ValueError("Invalid status")

        # Delegate creation to repository
        return self.tasks.create(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project_id,
        )

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def list_tasks(self, project_id: Optional[str] = None) -> List[Task]:
        return self.tasks.list(project_id=project_id)

    def edit_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> Task:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Task not found")

        if title:
            if len(title) > self.config.MAX_TASK_NAME_LENGTH:
                raise ValueError("Title too long")
            task.title = title

        if description:
            if len(description) > self.config.MAX_TASK_DESC_LENGTH:
                raise ValueError("Description too long")
            task.description = description

        if status:
            if status not in Task.VALID_STATUSES:
                raise ValueError("Invalid status")
            task.status = status

        if deadline:
            task.deadline = deadline

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: str) -> bool:
        task = self.get_task(task_id)
        if not task:
            raise ValueError("Task not found")

        self.tasks.delete(task)
        return True
