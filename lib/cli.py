from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag
from helpers import exit_program
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import ipdb


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
    console.print("  🏢 [cyan]list jobs[/cyan] - Show all job applications")
    console.print("  🖊️ [cyan]create job[/cyan] - Create a new job application")
    console.print("  ✏️ [cyan]update job[/cyan] - Update an existing job application")
    console.print("  ❌ [red]delete job[/red] - Delete a job application")
    console.print("  ❓ [cyan]help[/cyan] - See all available commands")
    console.print("[red]exit[/red] - Quit the application\n")

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
        elif command == "list jobs":
            list_jobs()
        elif command == "create job":
            create_job()
        elif command == "update job":
            update_job()
        elif command == "delete job":
            delete_job()
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
    print("  list jobs             - List all job applications")
    print("  create job            - Add a new job application")
    print("  update job            - Update an existing job application")
    print("  delete job            - Remove a job application")

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
    tag_type = input("Enter tag type (location or length): ").strip().lower()
    
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
    """Assign a tag to a job application via JobApplication."""
    job_id = input("Enter job application ID: ").strip()
    tag_id = input("Enter tag ID: ").strip()

    try:
        job_id, tag_id = int(job_id), int(tag_id)
        job = JobApplication.find_by_id(job_id)

        if not job:
            print(f"Job application ID {job_id} not found.")
            return
        
        job.add_tag(tag_id)
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

def list_jobs():
    """List all job applications."""
    jobs = JobApplication.get_all()
    if not jobs:
        print("No job applications found.")
    else:
        print("\nJob Applications:")
        for job in jobs:
            print(f"  Job ID {job.id}: {job.job_title} - {job.status}")

def create_job():
    """Prompt the user to create a new job application."""
    job_title = input("Enter job title: ").strip()
    
    company_name = input("Enter company name: ").strip()
    
    company = Company.find_by_name(company_name)
    
    if not company:
        print(f"No company found with the name '{company_name}'. Please ensure the company exists.")
        return
    
    description = input("Enter job description: ").strip()
    date_applied = input("Enter date applied (YYYY-MM-DD): ").strip()
    last_follow_up = input("Enter last follow-up date (YYYY-MM-DD or leave blank): ").strip()
    status = input("Enter job status (applied, pending, rejected, offer): ").strip()

    try:
        job = JobApplication(
            job_title=job_title,
            company_id=company.id,  # Use the company's ID
            description=description,
            date_applied=date_applied,
            last_follow_up=last_follow_up if last_follow_up else None,
            status=status
        )
        job.save()
    except ValueError as e:
        print(f"Error: {e}")


def update_job():
    """Prompt the user to update an existing job application."""
    job_id = input("Enter job application ID to update: ").strip()

    try:
        job_id = int(job_id)
        job = JobApplication.find_by_id(job_id)
        
        if not job:
            print(f"Job application with ID {job_id} not found.")
            return

        print(f"Updating job application: {job.job_title} at Company ID {job.company_id}")

        #
        job_title = input(f"Enter new job title (current: {job.job_title}): ").strip()
        company_name = input(f"Enter new company name (current: {job.company_id}): ").strip()

        # FETCH COMPANY WITH COMPANY NAME
        company = Company.find_by_name(company_name)

        if not company:
            print(f"No company found with the name '{company_name}'. Please ensure the company exists.")
            return

        description = input(f"Enter new job description (current: {job.description}): ").strip()
        date_applied = input(f"Enter new date applied (current: {job.date_applied}): ").strip()
        last_follow_up = input(f"Enter new last follow-up date (current: {job.last_follow_up} or leave blank): ").strip()
        status = input(f"Enter new status (current: {job.status}): ").strip()

        try:
            job.job_title = job_title if job_title else job.job_title
            job.company_id = company.id
            job.description = description if description else job.description
            job.date_applied = date_applied if date_applied else job.date_applied
            job.last_follow_up = last_follow_up if last_follow_up else job.last_follow_up
            job.status = status if status else job.status

            job.update()  # Call the update method to save changes
            print(f"Job application with ID {job_id} updated successfully.")
        except ValueError as e:
            print(f"Error: {e}")
    except ValueError:
        print("Invalid input. Please enter a valid job application ID.")



def delete_job():
    """Prompt the user to delete a job application."""
    job_id = input("Enter job application ID to delete: ").strip()
    try:
        job_id = int(job_id)
        job = JobApplication.find_by_id(job_id)
        if job:
            job.delete()
        else:
            print(f"Job application ID {job_id} not found.")
    except ValueError:
        print("Invalid input. Please enter a valid job ID.")

if __name__ == "__main__":
    main()