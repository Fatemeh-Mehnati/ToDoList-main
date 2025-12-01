# core/models/project.py
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from core.database import Base
import datetime
import uuid

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
