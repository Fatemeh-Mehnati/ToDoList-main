# core/repositories/project_repository.py
from typing import List, Optional
from sqlalchemy.orm import Session

from core.models.project import Project


class ProjectRepository:
    """Data access layer for Project model."""

    def __init__(self, db: Session) -> None:
        self.db = db

    # --- CREATE ---
    def create(self, name: str, description: Optional[str] = None) -> Project:
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    # --- READ ---
    def get(self, project_id: str) -> Optional[Project]:
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[Project]:
        return (
            self.db.query(Project)
            .filter(Project.name == name)
            .first()
        )

    def list(self) -> List[Project]:
        return (
            self.db.query(Project)
            .order_by(Project.created_at.desc())
            .all()
        )

    def count(self) -> int:
        return self.db.query(Project).count()

    # --- DELETE ---
    def delete(self, project: Project) -> None:
        self.db.delete(project)
        self.db.commit()
