# lib/cli.py
from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag
from helpers import exit_program
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def show_welcome():
    console.print(
        Panel.fit(
            Text("💼 Job Application Tracker 💼", style="bold cyan"),
            title="🚀 Welcome!", 
            border_style="green"
        )
    )

    console.print(
        "[bold green]Track your job applications, manage tags, and stay organized![/bold green]"
    )

    console.print("\n[bold yellow]Quick Commands:[/bold yellow]")
    console.print("  🎯 [cyan]add tag[/cyan] - Create a new tag")
    console.print("  📝 [cyan]list tags[/cyan] - Show all saved tags")
    console.print("  🔗 [cyan]attach tag[/cyan] - Link a tag to a job application")
    console.print("  ❓ [cyan]help[/cyan] - See all available commands")
    console.print("  ❌ [red]exit[/red] - Quit the application\n")



def main():
    show_welcome()

    while True:
        command = input("\nEnter a command: ").strip().lower()
        
        if command in ["exit", "quit"]:
            exit_program()
        elif command in ["help", "?"]:
            show_help()
        elif command == "list tags":
            list_tags()
        elif command == "create tag":
            create_tag()
        elif command == "delete tag":
            delete_tag()
        elif command == "assign tag":
            assign_tag_to_job()
        elif command == "remove tag":
            remove_tag_from_job()
        elif command == "list jobs by tag":
            list_jobs_by_tag()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")

def show_help():
    """Display available commands."""
    print("\nAvailable Commands:")
    print("  exit / quit           - Exit the program")
    print("  help / ?              - Show this help menu")
    print("  list tags             - Show all available tags")
    print("  create tag            - Add a new tag")
    print("  delete tag            - Remove a tag by ID")
    print("  assign tag            - Assign a tag to a job application")
    print("  remove tag            - Remove a tag from a job application")
    print("  list jobs by tag      - Show jobs associated with a tag")

def list_tags():
    """List all tags stored in the database."""
    tags = Tag.get_all()
    if not tags:
        print("No tags found.")
    else:
        print("\nTags:")
        for tag in tags:
            print(f"  {tag.id}: {tag.name} ({tag.tag_type})")

def create_tag():
    """Prompt the user to create a new tag."""
    name = input("Enter tag name: ").strip()
    tag_type = input("Enter tag type (location/length): ").strip().lower()
    
    if tag_type not in ["location", "length"]:
        print("Invalid tag type. Must be 'location' or 'length'.")
        return

    tag = Tag(name=name, tag_type=tag_type)
    tag.save()
    print(f"Tag '{name}' added successfully.")

def delete_tag():
    """Prompt the user to delete a tag."""
    list_tags()
    tag_id = input("Enter the tag ID to delete: ").strip()
    
    try:
        tag_id = int(tag_id)
        Tag.delete(tag_id)
        print(f"Tag {tag_id} deleted successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid tag ID.")

def assign_tag_to_job():
    """Assign a tag to a job application."""
    job_id = input("Enter job application ID: ").strip()
    tag_id = input("Enter tag ID: ").strip()
    
    try:
        job_id, tag_id = int(job_id), int(tag_id)
        JobApplicationTag(tag_id=tag_id, post_id=job_id).save()
        print(f"Tag {tag_id} assigned to job {job_id}.")
    except ValueError:
        print("Invalid input. Please enter valid numerical IDs.")

def remove_tag_from_job():
    """Remove a tag from a job application."""
    job_id = input("Enter job application ID: ").strip()
    tag_id = input("Enter tag ID: ").strip()
    
    try:
        job_id, tag_id = int(job_id), int(tag_id)
        JobApplicationTag.delete_tag_from_job(job_id, tag_id)
        print(f"Tag {tag_id} removed from job {job_id}.")
    except ValueError:
        print("Invalid input. Please enter valid numerical IDs.")

def list_jobs_by_tag():
    """List all job applications associated with a tag."""
    tag_id = input("Enter tag ID: ").strip()
    
    try:
        tag_id = int(tag_id)
        jobs = JobApplicationTag.get_jobs_by_tag(tag_id)
        if not jobs:
            print(f"No jobs found for tag {tag_id}.")
        else:
            print("\nJobs with this tag:")
            for job in jobs:
                print(f"  Job {job[0]}: {job[1]}")
    except ValueError:
        print("Invalid input. Please enter a valid tag ID.")

if __name__ == "__main__":
    main()



#PYTHONPATH=lib python -m cli
