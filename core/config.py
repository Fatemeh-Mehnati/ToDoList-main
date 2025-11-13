# core/config.py (بدون dotenv)
import os


class Config:
    """Configuration class for ToDoList application."""
    
    def __init__(self):
        # Project limits (with default values)
        self.MAX_PROJECTS = int(os.environ.get('MAX_PROJECTS', '10'))
        self.MAX_PROJECT_NAME_LENGTH = int(os.environ.get('MAX_PROJECT_NAME_LENGTH', '30'))
        self.MAX_PROJECT_DESC_LENGTH = int(os.environ.get('MAX_PROJECT_DESC_LENGTH', '150'))
        
        # Task limits
        self.MAX_TASKS_PER_PROJECT = int(os.environ.get('MAX_TASKS_PER_PROJECT', '20'))
        self.MAX_TASK_NAME_LENGTH = int(os.environ.get('MAX_TASK_NAME_LENGTH', '30'))
        self.MAX_TASK_DESC_LENGTH = int(os.environ.get('MAX_TASK_DESC_LENGTH', '150'))
    
    def __repr__(self):
        return (f"Config(MAX_PROJECTS={self.MAX_PROJECTS}, "
                f"MAX_TASKS_PER_PROJECT={self.MAX_TASKS_PER_PROJECT})")
