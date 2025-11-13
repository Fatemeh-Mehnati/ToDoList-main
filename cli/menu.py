# cli/menu.py
from cli import project_cli, task_cli


class Menu:
    """Menu management and user interface"""
    
    def __init__(self, manager):
        self.manager = manager
    
    def show_main_menu(self):
        """Display main menu"""
        while True:
            print("\n" + "="*50)
            print("🎯 Project and Task Management System")
            print("="*50)
            print("1. Manage Projects")
            print("2. Manage Tasks")
            print("0. Exit")
            print("-"*50)
            
            choice = input("Your choice: ").strip()
            
            if choice == '1':
                self.show_project_menu()
            elif choice == '2':
                self.show_task_menu()
            elif choice == '0':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def show_project_menu(self):
        """Display project management menu"""
        while True:
            print("\n" + "="*40)
            print("📁 Project Management")
            print("="*40)
            print("1. Create New Project")
            print("2. List Projects")
            print("3. Edit Project")
            print("4. Delete Project")
            print("0. Back to Main Menu")
            print("-"*40)
            
            choice = input("Your choice: ").strip()
            
            if choice == '1':
                project_cli.create_project(self.manager)
            elif choice == '2':
                project_cli.list_projects(self.manager)
            elif choice == '3':
                project_cli.edit_project(self.manager)
            elif choice == '4':
                project_cli.delete_project(self.manager)
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice! Please try again.")
    
    def show_task_menu(self):
        """Display task management menu"""
        while True:
            print("\n" + "="*40)
            print("📋 Task Management")
            print("="*40)
            print("1. Create New Task")
            print("2. List Tasks")
            print("3. Edit Task")
            print("4. Change Task Status")
            print("5. Delete Task")
            print("0. Back to Main Menu")
            print("-"*40)
            
            choice = input("Your choice: ").strip()
            
            if choice == '1':
                task_cli.create_task(self.manager)
            elif choice == '2':
                task_cli.list_tasks(self.manager)
            elif choice == '3':
                task_cli.edit_task(self.manager)
            elif choice == '4':
                task_cli.change_task_status(self.manager)
            elif choice == '5':
                task_cli.delete_task(self.manager)
            elif choice == '0':
                break
            else:
                print("❌ Invalid choice! Please try again.")
