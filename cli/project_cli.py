# cli/project_cli.py
from core.todo_manager import TodoManager


def create_project(manager: TodoManager):
    """Create a new project"""
    try:
        print("\n=== Create New Project ===")
        
        # Get project name
        name = input("Project name: ").strip()
        if not name:
            print("❌ Project name cannot be empty!")
            return
        
        # Get description
        description = input("Project description: ").strip()
        if not description:
            print("❌ Project description cannot be empty!")
            return
        
        # Create project
        project = manager.create_project(name, description)
        print(f"✅ Project '{project.name}' created successfully!")
        print(f"🆔 Project ID: {project.id}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def list_projects(manager: TodoManager):
    """Display list of projects"""
    try:
        print("\n=== Project List ===")
        
        projects = manager.list_projects()
        
        if not projects:
            print("📝 No projects found!")
            return
        
        print(f"📊 Total projects: {len(projects)}")
        print("-" * 80)
        
        for i, project in enumerate(projects, 1):
            print(f"{i}. Name: {project.name}")
            print(f"   🆔 ID: {project.id}")
            print(f"   📝 Description: {project.description}")
            print(f"   📋 Number of tasks: {len(project.tasks)}")
            print("-" * 40)
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def edit_project(manager: TodoManager):
    """Edit a project"""
    try:
        print("\n=== Edit Project ===")
        
        # Display list of projects
        projects = manager.list_projects()
        if not projects:
            print("📝 No projects available to edit!")
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
            
            selected_project = projects[choice]
            project_id = selected_project.id
            
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Get new information
        print(f"\nEditing project: {selected_project.name}")
        print("(Press Enter to skip)")
        
        new_name = input(f"New name [{selected_project.name}]: ").strip()
        new_description = input(f"New description [{selected_project.description}]: ").strip()
        
        # Apply changes
        name = new_name if new_name else None
        description = new_description if new_description else None
        
        if name or description:
            updated_project = manager.edit_project(project_id, name=name, description=description)
            print(f"✅ Project '{updated_project.name}' updated successfully!")
        else:
            print("ℹ️ No changes applied.")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


def delete_project(manager: TodoManager):
    """Delete a project"""
    try:
        print("\n=== Delete Project ===")
        
        # Display list of projects
        projects = manager.list_projects()
        if not projects:
            print("📝 No projects available to delete!")
            return
        
        print("Available projects:")
        for i, project in enumerate(projects, 1):
            print(f"{i}. {project.name} (ID: {project.id[:8]}...) - {len(project.tasks)} tasks")
        
        # Select project
        try:
            choice = int(input("\nProject number to delete: ")) - 1
            if choice < 0 or choice >= len(projects):
                print("❌ Invalid number!")
                return
            
            selected_project = projects[choice]
            
        except ValueError:
            print("❌ Please enter a valid number!")
            return
        
        # Confirm deletion
        confirm = input(f"⚠️ Are you sure you want to delete project '{selected_project.name}' and all its {len(selected_project.tasks)} tasks? (y/N): ").strip().lower()
        
        if confirm in ['y', 'yes']:
            manager.delete_project(selected_project.id)
            print(f"✅ Project '{selected_project.name}' deleted successfully!")
        else:
            print("❌ Delete operation cancelled.")
            
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
