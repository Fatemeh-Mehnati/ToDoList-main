# core/models/task.py
from sqlalchemy import Column, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
import datetime
import uuid

class Task(Base):
    __tablename__ = "tasks"

    VALID_STATUSES = ["todo", "in_progress", "done"]

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="todo", nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    deadline = Column(DateTime, nullable=True)

    # Foreign key to project
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=True)
    project = relationship("Project", back_populates="tasks")
