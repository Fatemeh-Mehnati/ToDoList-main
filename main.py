# main.py
from typing import Any
from core.services.todo_manager import TodoManager
from cli.menu import Menu
from core.database import SessionLocal
# Optional: If you want to auto-create tables every time the app runs:
# from core.create_tables import create_tables


def main() -> None:
    """Main program entry point"""
    # Optional: create tables
    # create_tables()

    # Create a database session
    db = SessionLocal()

    try:
        # Initialize TodoManager with the database session
        manager: TodoManager = TodoManager(db=db)

        # Create and display the main menu
        menu: Menu = Menu(manager)
        menu.show_main_menu()

    except KeyboardInterrupt:
        print("\n👋 Program exited successfully.")
    except Exception as e:
        # Keep this for debugging — later we can improve error handling
        print(f"❌ Unexpected error: {e}")
    finally:
        # Important: Close the database session
        db.close()


if __name__ == "__main__":
    main()
