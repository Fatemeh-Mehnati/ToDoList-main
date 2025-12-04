# core/services/todo_manager.py

from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from core.models.project import Project
from core.models.task import Task
from core.config import Config
from core.repositories.project_repository import ProjectRepository
from core.repositories.task_repository import TaskRepository
from core.services.validators import (
    validate_project_name,
    validate_project_description,
    validate_task_title,
    validate_task_description,
    validate_task_status,
)


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

        # Field-level validation
        validate_project_name(name, self.config)
        validate_project_description(description, self.config)

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

        if name is not None:
            # validate name
            validate_project_name(name, self.config)

            # Check for duplicate name (excluding this project)
            existing = (
                self.db.query(Project)
                .filter(Project.name == name, Project.id != project_id)
                .first()
            )
            if existing:
                raise ValueError(f"Project with name '{name}' already exists")

            project.name = name

        if description is not None:
            validate_project_description(description, self.config)
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

        # Field-level validation
        validate_task_title(title, self.config)
        validate_task_description(description, self.config)
        validate_task_status(status)

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

        if title is not None:
            validate_task_title(title, self.config)
            task.title = title

        if description is not None:
            validate_task_description(description, self.config)
            task.description = description

        if status is not None:
            validate_task_status(status)
            task.status = status

        if deadline is not None:
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

    def close_overdue_tasks(self) -> int:
        """
        Close all tasks whose deadline has passed and are not done yet.
        Returns the number of tasks that were updated.
        """
        now = datetime.utcnow()

        overdue_tasks = (
            self.db.query(Task)
            .filter(
                Task.deadline.isnot(None),
                Task.deadline < now,
                Task.status != "done",
            )
            .all()
        )

        for task in overdue_tasks:
            task.status = "done"

        self.db.commit()
        return len(overdue_tasks)
