# core/repositories/task_repository.py
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from core.models.task import Task


class TaskRepository:
    """Data access layer for Task model."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # --- CREATE ---
    def create(
        self,
        title: str,
        description: Optional[str] = None,
        status: str = "todo",
        deadline: Optional[datetime] = None,
        project_id: Optional[str] = None,
    ) -> Task:
        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project_id,
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # --- READ ---
    def get(self, task_id: str) -> Optional[Task]:
        return (
            self.db.query(Task)
            .filter(Task.id == task_id)
            .first()
        )

    def list(self, project_id: Optional[str] = None) -> List[Task]:
        query = self.db.query(Task)
        if project_id:
            query = query.filter(Task.project_id == project_id)
        return query.order_by(Task.created_at.desc()).all()

    def count_by_project(self, project_id: str) -> int:
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .count()
        )

    # --- DELETE ---
    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
