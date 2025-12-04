# commands/close_overdue_tasks.py

from core.database import SessionLocal
from core.services.todo_manager import TodoManager


def main() -> None:
    db = SessionLocal()
    try:
        manager = TodoManager(db=db)
        closed_count = manager.close_overdue_tasks()
        print(f"✅ Closed {closed_count} overdue tasks.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
