# core/todo_manager.py
from core.project import Project
from core.task import Task
from core.config import Config


class TodoManager:
    """Manage projects and tasks"""
    
    def __init__(self, config=None):
        self.config = config if config else Config()
        self.projects = []
        self.all_tasks = []  # Central list of all tasks
    
    # ==================== Project Management ====================
    
    def create_project(self, name, description):
        """Create a new project"""
        # Check project count limit
        if len(self.projects) >= self.config.MAX_PROJECTS:
            raise ValueError(f"Cannot create more than {self.config.MAX_PROJECTS} projects")
        
        # Check name length limit
        if len(name) > self.config.MAX_PROJECT_NAME_LENGTH:
            raise ValueError(f"Project name cannot exceed {self.config.MAX_PROJECT_NAME_LENGTH} characters")
        
        # Check description length limit
        if len(description) > self.config.MAX_PROJECT_DESC_LENGTH:
            raise ValueError(f"Project description cannot exceed {self.config.MAX_PROJECT_DESC_LENGTH} characters")
        
        # Check for duplicate name
        if any(p.name == name for p in self.projects):
            raise ValueError(f"Project with name '{name}' already exists")
        
        # Create project
        project = Project(name=name, description=description)
        self.projects.append(project)
        return project
    
    def get_project(self, project_id):
        """Get project by ID"""
        for project in self.projects:
            if project.id == project_id:
                return project
        return None
    
    def list_projects(self):
        """List all projects"""
        return self.projects
    
    def edit_project(self, project_id, name=None, description=None):
        """Edit project"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")
        
        # Check constraints
        if name:
            if len(name) > self.config.MAX_PROJECT_NAME_LENGTH:
                raise ValueError(f"Project name cannot exceed {self.config.MAX_PROJECT_NAME_LENGTH} characters")
            if any(p.name == name and p.id != project_id for p in self.projects):
                raise ValueError(f"Project with name '{name}' already exists")
        
        if description and len(description) > self.config.MAX_PROJECT_DESC_LENGTH:
            raise ValueError(f"Project description cannot exceed {self.config.MAX_PROJECT_DESC_LENGTH} characters")
        
        project.edit(name=name, description=description)
        return project
    
    def delete_project(self, project_id):
        """Delete project (Cascade Delete)"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")
        
        # Delete all tasks of the project from the central list
        task_ids = [task.id for task in project.tasks]
        self.all_tasks = [t for t in self.all_tasks if t.id not in task_ids]
        
        # Delete project
        self.projects.remove(project)
        return True
    
    # ==================== Task Management ====================
    
    def create_task(self, project_id, title, description, status='todo', deadline=None):
        """Create a new task"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")
        
        # Check task count limit
        if len(project.tasks) >= self.config.MAX_TASKS_PER_PROJECT:
            raise ValueError(f"Cannot create more than {self.config.MAX_TASKS_PER_PROJECT} tasks per project")
        
        # Check length limit
        if len(title) > self.config.MAX_TASK_NAME_LENGTH:
            raise ValueError(f"Task title cannot exceed {self.config.MAX_TASK_NAME_LENGTH} characters")
        
        if len(description) > self.config.MAX_TASK_DESC_LENGTH:
            raise ValueError(f"Task description cannot exceed {self.config.MAX_TASK_DESC_LENGTH} characters")
        
        # Check valid status
        if status not in ['todo', 'in_progress', 'done']:
            raise ValueError("Status must be one of: todo, in_progress, done")
        
        # Create task
        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project_id
        )
        
        # Add to project and central list
        project.add_task(task)
        self.all_tasks.append(task)
        
        return task
    
    def get_task(self, task_id):
        """Get task by ID"""
        for task in self.all_tasks:
            if task.id == task_id:
                return task
        return None
    
    def list_tasks(self, project_id=None):
        """List tasks (all or just one project)"""
        if project_id:
            project = self.get_project(project_id)
            if not project:
                raise ValueError(f"Project with ID '{project_id}' not found")
            return project.tasks
        return self.all_tasks
    
    def edit_task(self, task_id, title=None, description=None, status=None, deadline=None):
        """Edit task"""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")
        
        # Check constraints
        if title and len(title) > self.config.MAX_TASK_NAME_LENGTH:
            raise ValueError(f"Task title cannot exceed {self.config.MAX_TASK_NAME_LENGTH} characters")
        
        if description and len(description) > self.config.MAX_TASK_DESC_LENGTH:
            raise ValueError(f"Task description cannot exceed {self.config.MAX_TASK_DESC_LENGTH} characters")
        
        if status and status not in ['todo', 'in_progress', 'done']:
            raise ValueError("Status must be one of: todo, in_progress, done")
        
        task.edit(title=title, description=description, status=status, deadline=deadline)
        return task
    
    def delete_task(self, task_id):
        """Delete task"""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")
        
        # Delete from project
        project = self.get_project(task.project_id)
        if project:
            project.remove_task(task_id)
        
        # Delete from central list
        self.all_tasks.remove(task)
        return True
