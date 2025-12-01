# core/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings   # فرض: settings.DATABASE_URL هست

DATABASE_URL = settings.DATABASE_URL  # مثل: postgresql://user:pass@db:5432/todolist

# اگر می‌خوای لاگ SQL ببینی، echo=True بذار
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

# Base class for ORM models
Base = declarative_base()
