# ...existing code...
# core/task.py
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    # Avoid runtime circular imports; only for type hints
    from .project import Project


class Task:
    """Represents a task in the ToDoList."""

    VALID_STATUSES = ["todo", "in_progress", "done"]

    id: str
    title: str
    description: str
    status: str
    created_at: datetime
    deadline: Optional[datetime]
    project_id: Optional[str]

    def __init__(
        self,
        title: str,
        description: str = "",
        status: str = "todo",
        deadline: Optional[datetime] = None,
        project_id: Optional[str] = None,
    ) -> None:
        if len(title) > 50:
            raise ValueError("Task title cannot exceed 50 characters.")
        if len(description) > 200:
            raise ValueError("Task description cannot exceed 200 characters.")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")

        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.status = status
        self.created_at = datetime.now()
        self.deadline = deadline
        self.project_id = project_id

    def update_status(self, new_status: str) -> None:
        """Change task status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.status = new_status

    def update_title(self, new_title: str) -> None:
        """Change task title"""
        if len(new_title) > 50:
            raise ValueError("Task title cannot exceed 50 characters.")
        self.title = new_title

    def update_description(self, new_description: str) -> None:
        """Change task description"""
        if len(new_description) > 200:
            raise ValueError("Task description cannot exceed 200 characters.")
        self.description = new_description

    def set_deadline(self, new_deadline: Optional[datetime]) -> None:
        """Set or clear the deadline"""
        self.deadline = new_deadline

    def edit(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        deadline: Optional[datetime] = None,
    ) -> None:
        """Edit multiple fields at once (used by manager)"""
        if title is not None:
            self.update_title(title)
        if description is not None:
            self.update_description(description)
        if status is not None:
            self.update_status(status)
        if deadline is not None:
            self.set_deadline(deadline)

    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"

    def __str__(self) -> str:
        return f"[{self.status}] {self.title}"
# ...existing code...