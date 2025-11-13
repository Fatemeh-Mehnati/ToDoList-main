# main.py
from core.todo_manager import TodoManager
from cli.menu import Menu


def main():
    """Main program function"""
    try:
        # Create task manager
        manager = TodoManager()
        
        # Create menu
        menu = Menu(manager)
        
        # Show main menu
        menu.show_main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Program closed successfully!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
