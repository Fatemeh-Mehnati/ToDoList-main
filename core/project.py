# ...existing code...
# core/project.py
import uuid
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from .task import Task  # for type checking only


class Project:
    """Represents a project in the ToDoList."""

    id: str
    name: str
    description: str
    tasks: List["Task"]

    def __init__(self, name: str, description: str, id: Optional[str] = None) -> None:
        """
        Args:
            name: Project name
            description: Project description
            id: Project ID (if None, a new UUID is generated)
        """
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.description = description
        self.tasks = []

    def add_task(self, task: "Task") -> None:
        """Add a new task to the project"""
        self.tasks.append(task)

    def remove_task(self, task_id: str) -> None:
        """Remove a task by its ID (Cascade Delete)"""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def edit(self, name: Optional[str] = None, description: Optional[str] = None) -> None:
        """Edit the project's name and description"""
        if name:
            self.name = name
        if description:
            self.description = description

    def __repr__(self) -> str:
        return f"Project(id={self.id}, name='{self.name}', description='{self.description}', tasks={len(self.tasks)})"
# ...existing code...