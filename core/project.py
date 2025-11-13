# core/project.py
import uuid


class Project:
    """نماینده‌ی یک پروژه در ToDoList"""

    def __init__(self, name, description, id=None):
        """
        Args:
            name: نام پروژه
            description: توضیحات پروژه
            id: شناسه پروژه (اگر None باشه، UUID جدید می‌سازه)
        """
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.description = description
        self.tasks = []

    def add_task(self, task):
        """افزودن تسک جدید به پروژه"""
        self.tasks.append(task)

    def remove_task(self, task_id):
        """حذف تسک بر اساس شناسه (Cascade Delete)"""
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def edit(self, name=None, description=None):
        """ویرایش نام و توضیح پروژه"""
        if name:
            self.name = name
        if description:
            self.description = description

    def __repr__(self):
        return f"Project(id={self.id}, name='{self.name}', description='{self.description}', tasks={len(self.tasks)})"
