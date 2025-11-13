# core/todo_manager.py
from core.project import Project
from core.task import Task
from core.config import Config


class TodoManager:
    """مدیریت پروژه‌ها و تسک‌ها"""
    
    def __init__(self, config=None):
        self.config = config if config else Config()
        self.projects = []
        self.all_tasks = []  # لیست مرکزی تمام تسک‌ها
    
    # ==================== Project Management ====================
    
    def create_project(self, name, description):
        """ساخت پروژه جدید"""
        # بررسی محدودیت تعداد
        if len(self.projects) >= self.config.MAX_PROJECTS:
            raise ValueError(f"Cannot create more than {self.config.MAX_PROJECTS} projects")
        
        # بررسی محدودیت طول نام
        if len(name) > self.config.MAX_PROJECT_NAME_LENGTH:
            raise ValueError(f"Project name cannot exceed {self.config.MAX_PROJECT_NAME_LENGTH} characters")
        
        # بررسی محدودیت طول توضیحات
        if len(description) > self.config.MAX_PROJECT_DESC_LENGTH:
            raise ValueError(f"Project description cannot exceed {self.config.MAX_PROJECT_DESC_LENGTH} characters")
        
        # بررسی تکراری نبودن نام
        if any(p.name == name for p in self.projects):
            raise ValueError(f"Project with name '{name}' already exists")
        
        # ساخت پروژه
        project = Project(name=name, description=description)
        self.projects.append(project)
        return project
    
    def get_project(self, project_id):
        """دریافت پروژه بر اساس ID"""
        for project in self.projects:
            if project.id == project_id:
                return project
        return None
    
    def list_projects(self):
        """لیست تمام پروژه‌ها"""
        return self.projects
    
    def edit_project(self, project_id, name=None, description=None):
        """ویرایش پروژه"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")
        
        # بررسی محدودیت‌ها
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
        """حذف پروژه (Cascade Delete)"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")
        
        # حذف تمام تسک‌های پروژه از لیست مرکزی
        task_ids = [task.id for task in project.tasks]
        self.all_tasks = [t for t in self.all_tasks if t.id not in task_ids]
        
        # حذف پروژه
        self.projects.remove(project)
        return True
    
    # ==================== Task Management ====================
    
    def create_task(self, project_id, title, description, status='todo', deadline=None):
        """ساخت تسک جدید"""
        project = self.get_project(project_id)
        if not project:
            raise ValueError(f"Project with ID '{project_id}' not found")
        
        # بررسی محدودیت تعداد تسک‌ها
        if len(project.tasks) >= self.config.MAX_TASKS_PER_PROJECT:
            raise ValueError(f"Cannot create more than {self.config.MAX_TASKS_PER_PROJECT} tasks per project")
        
        # بررسی محدودیت طول
        if len(title) > self.config.MAX_TASK_NAME_LENGTH:
            raise ValueError(f"Task title cannot exceed {self.config.MAX_TASK_NAME_LENGTH} characters")
        
        if len(description) > self.config.MAX_TASK_DESC_LENGTH:
            raise ValueError(f"Task description cannot exceed {self.config.MAX_TASK_DESC_LENGTH} characters")
        
        # بررسی وضعیت معتبر
        if status not in ['todo', 'in_progress', 'done']:
            raise ValueError("Status must be one of: todo, in_progress, done")
        
        # ساخت تسک
        task = Task(
            title=title,
            description=description,
            status=status,
            deadline=deadline,
            project_id=project_id
        )
        
        # افزودن به پروژه و لیست مرکزی
        project.add_task(task)
        self.all_tasks.append(task)
        
        return task
    
    def get_task(self, task_id):
        """دریافت تسک بر اساس ID"""
        for task in self.all_tasks:
            if task.id == task_id:
                return task
        return None
    
    def list_tasks(self, project_id=None):
        """لیست تسک‌ها (همه یا فقط یک پروژه)"""
        if project_id:
            project = self.get_project(project_id)
            if not project:
                raise ValueError(f"Project with ID '{project_id}' not found")
            return project.tasks
        return self.all_tasks
    
    def edit_task(self, task_id, title=None, description=None, status=None, deadline=None):
        """ویرایش تسک"""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")
        
        # بررسی محدودیت‌ها
        if title and len(title) > self.config.MAX_TASK_NAME_LENGTH:
            raise ValueError(f"Task title cannot exceed {self.config.MAX_TASK_NAME_LENGTH} characters")
        
        if description and len(description) > self.config.MAX_TASK_DESC_LENGTH:
            raise ValueError(f"Task description cannot exceed {self.config.MAX_TASK_DESC_LENGTH} characters")
        
        if status and status not in ['todo', 'in_progress', 'done']:
            raise ValueError("Status must be one of: todo, in_progress, done")
        
        task.edit(title=title, description=description, status=status, deadline=deadline)
        return task
    
    def delete_task(self, task_id):
        """حذف تسک"""
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task with ID '{task_id}' not found")
        
        # حذف از پروژه
        project = self.get_project(task.project_id)
        if project:
            project.remove_task(task_id)
        
        # حذف از لیست مرکزی
        self.all_tasks.remove(task)
        return True
