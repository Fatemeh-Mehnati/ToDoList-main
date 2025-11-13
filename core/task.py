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

    """نماینده‌ی یک تسک در ToDoList"""
    
    VALID_STATUSES = ["todo", "in_progress", "done"]
    
    def __init__(self, title: str, description: str = "", status: str = "todo"):
        if len(title) > 50:
            raise ValueError("عنوان تسک نمی‌تواند بیش از ۵۰ کاراکتر باشد")
        if len(description) > 200:
            raise ValueError("توضیحات تسک نمی‌تواند بیش از ۲۰۰ کاراکتر باشد")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"وضعیت باید یکی از {self.VALID_STATUSES} باشد")
        
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.status: str = status
        self.created_at: datetime = datetime.now()
        self.project_id: Optional[str] = None
    
    def update_status(self, new_status: str) -> None:
        """تغییر وضعیت تسک"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"وضعیت باید یکی از {self.VALID_STATUSES} باشد")
        self.status = new_status
    
    def update_title(self, new_title: str) -> None:
        """تغییر عنوان تسک"""
        if len(new_title) > 50:
            raise ValueError("عنوان تسک نمی‌تواند بیش از ۵۰ کاراکتر باشد")
        self.title = new_title
    
    def update_description(self, new_description: str) -> None:
        """تغییر توضیحات تسک"""
        if len(new_description) > 200:
            raise ValueError("توضیحات تسک نمی‌تواند بیش از ۲۰۰ کاراکتر باشد")
        self.description = new_description
    
    def __repr__(self) -> str:
        return f"Task(id={self.id}, title='{self.title}', status='{self.status}')"
    
    def __str__(self) -> str:
        return f"[{self.status}] {self.title}"
