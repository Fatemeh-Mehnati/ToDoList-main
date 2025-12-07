# app/api/dependencies.py

from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from core.database import SessionLocal
from core.services.todo_manager import TodoManager


def get_db() -> Generator[Session, None, None]:
    """Provide a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_todo_manager(db: Session = Depends(get_db)) -> TodoManager:
    """Provide a TodoManager instance per request."""
    return TodoManager(db=db)
