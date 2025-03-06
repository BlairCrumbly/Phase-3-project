from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag
from helpers import exit_program
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.table import Table
import ipdb
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.styles import Style



#returns a table for all jobs and and all companies, etc
#reprint menu when optimal
#multiple excepts for as many specific errors as possible
#look up a list of jobs by company

console = Console()
custom_style = Style.from_dict(
    {
        "dialog": "bg:#ffffff", 
        "dialog frame.label": "bg:#444488 bold",  # Title bar with a blue tint
        "dialog.body": "bg:#333333",  # Slightly lighter gray background
        "menu": "bg:#444444",  # Custom menu background (corrected)
        "radio.selected": "fg:#00ff00 bold",  # Selected item in bright green
        "radio": "fg:#cccccc",  # Normal text color for menu items
    }
)
def show_welcome():
    console.print(
            Panel.fit(
                Text("💼 Job Application Tracker 💼", style="bold cyan"),
                title="🚀 Welcome!", 
                border_style="green"
            )
        )

    console.print(
            Panel(
                "[bold cyan]Track your job applications, manage tags, and stay organized![/bold cyan]"
            )
        )
    return radiolist_dialog(
        title="📋 Job Tracker Menu",
        text="Use ↑↓ to navigate, Enter to select:",
        values=[
            ("list_jobs", "💼 List Jobs"),
            ("list_companies", "📊 List Companies"),
            ("create_job", "🖊️ Create Job"),
            ("help", "❓ Help"),
            ("exit", "👋 Exit"),
        ],
        style=custom_style,  # Apply the custom style
    ).run()


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
        elif command == "list companies":
            show_companies()
        elif command == "create company":
            create_company()
        elif command == "update company":
            update_company()
        elif command == "delete company":
            delete_company()
        else:
            print("Invalid command. Type 'help' for a list of available commands.")


def show_help():
    """Display available commands in a table format."""
    console = Console()
    table = Table(title="Available Commands", show_header=True, header_style="bold cyan")

    table.add_column("Command", style="bold orange")
    table.add_column("Description", style="white")

    commands = [
        ("exit / quit", "Exit the program"),
        ("help / ?", "Show this help menu"),
        ("list tags", "Show all available tags"),
        ("create tag", "Add a new tag"),
        ("delete tag", "Remove a tag by ID"),
        ("assign tag", "Assign a tag to a job application"),
        ("remove tag", "Remove a tag from a job application"),
        ("list jobs by tag", "Show jobs associated with a tag"),
        ("list jobs", "List all job applications"),
        ("create job", "Add a new job application"),
        ("update job", "Update an existing job application"),
        ("delete job", "Remove a job application"),
        ("list companies", "Show all companies"),
        ("create company", "Add a new company"),
        ("update company", "Update an existing company"),
        ("delete company", "Remove a company"),
    ]

    for command, description in commands:
        table.add_row(command, description)

    console.print(table)

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
    try:
        name = input("Enter tag name: ").strip()
        tag_type = input("Enter tag type (location or length): ").strip().lower()
        
        if tag_type not in ["location", "length"]:
            raise ValueError("Invalid tag type. Must be 'location' or 'length'.")

        tag = Tag(name=name, tag_type=tag_type)
        
        tag.save()
        if tag.id:
            print(f"Tag '{name}' added successfully.")

    except ValueError as ve:
        print(f"ValueError: {ve}")
    except AttributeError as ae:
        print(f"AttributeError: {ae} - Check if yourinputs are correctly formatted.")
    except TypeError as te:
        print(f"TypeError: {te} - Unexpected data type encountered.")
    except Exception as e:
        print(f"Unexpected error: {e}")

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
        print(f"No company found with the name '{company_name}'")
        question = input("Would you like to create a company? (Y/N)").strip()
        if question.upper() == "Y":
            website = input("Enter company website: ").strip()
            contact_info = input("Enter company contact info: ").strip()
            company = Company(name = company_name, website=website or None, contact_info=contact_info or None)
            company.save()
            print(f"{company.name} created successfully!")
        else:
            return
    
    description = input("Enter job description: ").strip()
    while True:
        date_applied_str = input("Enter date applied (YYYY-MM-DD): ").strip()
        try:
            date_applied = datetime.strptime(date_applied_str, "%Y-%m-%d").date()
            break  # Valid date, exit loop
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")

    
    last_follow_up = None
    while True:
        last_follow_up_str = input("Enter last follow-up date (YYYY-MM-DD or leave blank): ").strip()
        if not last_follow_up_str:
            break #PROCEED
        try:
            last_follow_up = datetime.strptime(last_follow_up_str, "%Y-%m-%d").date()
            if last_follow_up < date_applied:
                print("Last follow-up date cannot be before the date applied. Please enter a valid date.")
            else:
                break  #EXIT LOOP
        except ValueError:
            print("Invalid date format. Please enter the date in YYYY-MM-DD format.")


    valid_statuses = ["applied", "pending", "rejected", "offer"]
    status = input("Enter job status (applied, pending, rejected, offer): ").strip().lower()
    
    while status not in valid_statuses:
        print("Invalid status. Please enter one of the following: applied, pending, rejected, offer.")
        status = input("Enter job status (applied, pending, rejected, offer): ").strip().lower()

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


def show_companies():
    """List all companies stored in the database."""
    companies = Company.get_all()
    if companies:
        print("Companies: ")
        for company in companies:
            print(f"{company.id}: {company.name}")
    else:
        print("No companies found.")

def create_company():
    """Prompt user to create new company"""
    name = input("Enter company name: ")
    website = input("Enter company website: ")
    contact_info = input("Enter company contact info: ")

    company = Company(name = name, website=website or None, contact_info=contact_info or None)
    company.save()
    print(f"{company.name} created successfully!")

def update_company():
    company_id = input("enter the company ID you want to update: ").strip()

    try:
        company_id = int(company_id)
        company = Company.find_by_id(company_id)
        if not company:
            print(f"Comapny with ID: {company_id} not found.")
            return
        print(f"Updating company: {company.name}")
        name = input(f"Enter new name (current: {company.name}): ").strip()
        website = input(f"Enter new website (current: {company.website}): ").strip()
        contact_info = input(f"Enter new contact info (current: {company.contact_info}): ").strip()

        company.name = name if name else company.name
        company.website = website if website else company.website
        company.contact_info = contact_info if contact_info else company.contact_info
    except ValueError:
        print("Invalid input. Please enter a valid company ID.")

def delete_company():
    """Prompt the user to delete a company."""
    company_id = input("Enter the company ID to delete: ").strip()

    try:
        company_id = int(company_id)
        
        # Ensure the companies table exists before querying it
        Company.create_table()
        
        company = Company.find_by_id(company_id)
        
        if isinstance(company, Company):
            company.delete()
            print(f"Company with ID {company_id} ({company.name}) deleted successfully.")
        elif company is None:
            print(f"Company with ID {company_id} not found.")
        else:
            print(f"Error: {company}")  # If the returned result is an error message
    except ValueError:
        print("Invalid input. Please enter a valid company ID.")






if __name__ == "__main__":
    main()