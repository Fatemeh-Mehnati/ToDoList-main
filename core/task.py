# core/task.py
from typing import Optional
from datetime import datetime
import uuid


class Task:
    def __init__(self, title: str, description: str, completed: bool = False, deadline: str | None = None):
        self.title = title
        self.description = description
        self.completed = completed
        self.deadline = deadline

    """Represents a task in the ToDoList."""
    
    VALID_STATUSES = ["todo", "in_progress", "done"]
    
    def __init__(self, title: str, description: str = "", status: str = "todo"):
        if len(title) > 50:
            raise ValueError("Task title cannot exceed 50 characters.")
        if len(description) > 200:
            raise ValueError("Task description cannot exceed 200 characters.")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.status: str = status
        self.created_at: datetime = datetime.now()
        self.project_id: Optional[str] = None
    
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
    
    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def __str__(self) -> str:
        return f"[{self.status}] {self.title}"
