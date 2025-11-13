# cli/task_cli.py
from core.todo_manager import TodoManager
from datetime import datetime


def create_task(manager: TodoManager):
    """Create a new task"""
    try:
        print("\n=== Create New Task ===")
        
        # Display projects
        projects = manager.list_projects()
        if not projects:
            print("❌ No projects found! Please create a project first.")
            return
        
        print("Available projects:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project.name} (ID: {project.id[:8]}...)")
        
        # Select project
        try:
            choice = int(input("\nProject number: ")) - 1
            if choice < 0 or choice >= len(projects):
                print("❌ Invalid number!")
                return
            project_id = projects[choice].id
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Get task information
        title = input("Task title: ").strip()
        if not title:
            print("❌ Task title cannot be empty!")
            return
        
        description = input("Task description: ").strip()
        if not description:
            print("❌ Task description cannot be empty!")
            return
        
        # Get status
        print("\nStatus options:")
        print("1. Todo")
        print("2. In Progress")
        print("3. Done")
        status_choice = input("Status (default: todo): ").strip()
        
        status_map = {'1': 'todo', '2': 'in_progress', '3': 'done'}
        status = status_map.get(status_choice, 'todo')
        
        # Get deadline (optional)
        deadline_str = input("Deadline (YYYY-MM-DD) or press Enter to skip: ").strip()
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("⚠️ Invalid date format! Continuing without deadline.")
        
        # Create task
        task = manager.create_task(project_id, title, description, status, deadline)
        print(f"✅ Task '{task.title}' created successfully!")
        print(f"🆔 Task ID: {task.id}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def list_tasks(manager: TodoManager):
    """Display list of tasks"""
    try:
        print("\n=== Task List ===")
        
        # Ask filter option
        print("1. Show all tasks")
        print("2. Show tasks of a specific project")
        choice = input("Your choice (default: 1): ").strip()
        
        project_id = None
        if choice == '2':
            projects = manager.list_projects()
            if not projects:
                print("❌ No projects found!")
                return
            
            print("\nAvailable projects:")
            for i, project in enumerate(projects, 1):
                print(f"{i}. {project.name}")
            
            try:
                proj_choice = int(input("\nProject number: ")) - 1
                if 0 <= proj_choice < len(projects):
                    project_id = projects[proj_choice].id
            except ValueError:
                print("❌ Invalid number!")
                return
        
        # Get tasks
        tasks = manager.list_tasks(project_id)
        
        if not tasks:
            print("📝 No tasks found!")
            return
        
        print(f"\n📊 Total tasks: {len(tasks)}")
        print("-" * 80)
        
        for i, task in enumerate(tasks, 1):
            status_emoji = {'todo': '📝', 'in_progress': '🔄', 'done': '✅'}
            print(f"{i}. {status_emoji.get(task.status, '📝')} {task.title}")
            print(f"   🆔 ID: {task.id}")
            print(f"   📝 Description: {task.description}")
            print(f"   📊 Status: {task.status}")
            if task.deadline:
                print(f"   📅 Deadline: {task.deadline.strftime('%Y-%m-%d')}")
            print(f"   📁 Project ID: {task.project_id[:8]}...")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def edit_task(manager: TodoManager):
    """Edit a task"""
    try:
        print("\n=== Edit Task ===")
        
        # Display tasks
        tasks = manager.list_tasks()
        if not tasks:
            print("📝 No tasks available to edit!")
            return
        
        print("Available tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.title} (ID: {task.id[:8]}...) - {task.status}")
        
        # Select task
        try:
            choice = int(input("\nTask number: ")) - 1
            if choice < 0 or choice >= len(tasks):
                print("❌ Invalid number!")
                return
            
            selected_task = tasks[choice]
            task_id = selected_task.id
            
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Get new information
        print(f"\nEditing task: {selected_task.title}")
        print("(Press Enter to skip)")
        
        new_title = input(f"New title [{selected_task.title}]: ").strip()
        new_description = input(f"New description [{selected_task.description}]: ").strip()
        
        # Status
        print("\nStatus options:")
        print("1. Todo")
        print("2. In Progress")
        print("3. Done")
        print(f"Current: {selected_task.status}")
        status_choice = input("New status (press Enter to skip): ").strip()
        
        status_map = {'1': 'todo', '2': 'in_progress', '3': 'done'}
        new_status = status_map.get(status_choice)
        
        # Deadline
        deadline_str = input(f"New deadline (YYYY-MM-DD) or press Enter to skip: ").strip()
        new_deadline = None
        if deadline_str:
            try:
                new_deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
            except ValueError:
                print("⚠️ Invalid date format! Skipping deadline.")
        
        # Apply changes
        title = new_title if new_title else None
        description = new_description if new_description else None
        status = new_status
        deadline = new_deadline
        
        if title or description or status or deadline:
            updated_task = manager.edit_task(task_id, title=title, description=description, 
                                            status=status, deadline=deadline)
            print(f"✅ Task '{updated_task.title}' updated successfully!")
        else:
            print("ℹ️ No changes applied.")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def change_task_status(manager: TodoManager):
    """Change task status"""
    try:
        print("\n=== Change Task Status ===")
        
        # Display tasks
        tasks = manager.list_tasks()
        if not tasks:
            print("📝 No tasks available!")
            return
        
        print("Available tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.title} - Current status: {task.status}")
        
        # Select task
        try:
            choice = int(input("\nTask number: ")) - 1
            if choice < 0 or choice >= len(tasks):
                print("❌ Invalid number!")
                return
            
            selected_task = tasks[choice]
            
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Select new status
        print("\nNew status:")
        print("1. Todo")
        print("2. In Progress")
        print("3. Done")
        status_choice = input("Your choice: ").strip()
        
        status_map = {'1': 'todo', '2': 'in_progress', '3': 'done'}
        new_status = status_map.get(status_choice)
        
        if not new_status:
            print("❌ Invalid choice!")
            return
        
        # Apply change
        updated_task = manager.edit_task(selected_task.id, status=new_status)
        print(f"✅ Task status changed to: {updated_task.status}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def delete_task(manager: TodoManager):
    """Delete a task"""
    try:
        print("\n=== Delete Task ===")
        
        # Display tasks
        tasks = manager.list_tasks()
        if not tasks:
            print("📝 No tasks available to delete!")
            return
        
        print("Available tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task.title} (ID: {task.id[:8]}...) - {task.status}")
        
        # Select task
        try:
            choice = int(input("\nTask number to delete: ")) - 1
            if choice < 0 or choice >= len(tasks):
                print("❌ Invalid number!")
                return
            
            selected_task = tasks[choice]
            
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Confirm deletion
        confirm = input(f"⚠️ Are you sure you want to delete task '{selected_task.title}'? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            manager.delete_task(selected_task.id)
            print(f"✅ Task '{selected_task.title}' deleted successfully!")
        else:
            print("❌ Delete operation cancelled.")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
