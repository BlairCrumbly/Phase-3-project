# cli.py
from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from helpers import Helpers

class CLI:
    def __init__(self):
        self.console = Console()
        self.helpers = Helpers()
        self.command_handlers = {
            "exit": self.exit_program,
            "quit": self.exit_program,
            "help": self.show_help,
            "?": self.show_help,
            "list tags": self.list_tags,
            "create tag": self.create_tag,
            "delete tag": self.delete_tag,
            "assign tag": self.assign_tag_to_job,
            "remove tag": self.remove_tag_from_job,
            "list jobs by tag": self.list_jobs_by_tag,
            "list jobs": self.list_jobs,
            "create job": self.create_job,
            "update job": self.update_job,
            "delete job": self.delete_job,
            "list companies": self.list_companies,
            "create company": self.create_company,
            "update company": self.update_company,
            "delete company": self.delete_company,
        }

    def start(self):
        """Start the CLI application."""
        self.show_welcome()
        self.command_loop()

    def command_loop(self):
        """Main command processing loop."""
        while True:
            command = input("\n🏠 Enter a command: ").strip().lower()
            
            if command in self.command_handlers:
                self.command_handlers[command]()
            else:
                print("Invalid command. Type 'help' for a list of available commands.")

    def show_welcome(self):
        """Display the welcome message and quick commands in a table format."""
        self.console.print(
            Panel.fit(
                Text("💼 Job Application Tracker 💼", style="bold cyan"),
                title="🚀 Welcome!", 
                border_style="green"
            )
        )

        self.console.print(
            "[bold green]Track your job applications, manage tags, and stay organized![/bold green]"
        )

        table = Table(show_header=True, header_style="bold cyan", title="Quick Commands")
        table.add_column("Command", style="bold green")
        table.add_column("Description", style="white")

        commands = [
            ("💼 list jobs", "Show all job applications"),
            ("📊 list companies", "Show all job companies"),
            ("🖊️ create job", "Create a new job application"),
            ("❓ [yellow]help[/yellow]", "See all available commands"),
            ("👋[red] exit[/red]", "Quit the application"),
        ]

        for command, description in commands:
            table.add_row(command, description)

        self.console.print(table)

    def exit_program(self):
        """Exit the program."""
        print("👋 Thank you for using Job Application Tracker. Goodbye!")
        exit()

    def show_help(self):
        """Display available commands in a table format."""
        table = Table(title="Available Commands", show_header=True, header_style="bold cyan")

        table.add_column("Command", style="bold yellow")
        table.add_column("Description", style="white")

        commands = [
            ("exit / quit", "Exit the program"),
            ("help / ?", "Show this help menu"),
            ("list tags", "Show all available tags"),
            ("create tag", "Add a new tag"),
            ("delete tag", "Remove a tag by ID"),
            ("assign tag", "Assign a tag to a job application"),
            ("remove tag", "Remove a tag from a job application"),
            ("list jobs", "List all job applications"),
            ("list jobs by tag", "Show jobs associated with a tag"),
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

        self.console.print(table)

    def list_tags(self):
        """List all tags stored in the database."""
        tags = Tag.get_all()
        if not tags:
            print("No tags found.")
        else:
            print("\nTags:")
            for tag in tags:
                print(f"  {tag.id}: {tag.name} ({tag.tag_type})")

    def create_tag(self):
        """Prompt the user to create a new tag."""
        try:
            name = input("Enter tag name: ").strip().capitalize()
            tag_type = input("Enter tag type (location or length): ").strip().capitalize()
            
            if tag_type not in ["location", "length"]:
                raise ValueError("Invalid tag type. Must be 'location' or 'length'.")

            tag = Tag(name=name, tag_type=tag_type)
            
            tag.save()
            if tag.id:
                print(f"Tag '{name}' added successfully.")

        except ValueError as ve:
            print(f"ValueError: {ve}")
        except AttributeError as ae:
            print(f"AttributeError: {ae} - Check if your inputs are correctly formatted.")
        except TypeError as te:
            print(f"TypeError: {te} - Unexpected data type encountered.")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def delete_tag(self):
        """Prompt the user to delete a tag."""
        self.list_tags()
        tag_id = input("Enter the tag ID to delete: ").strip()
        
        try:
            tag_id = int(tag_id)
            Tag.delete(tag_id)
            print(f"Tag {tag_id} deleted successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid tag ID.")

    def assign_tag_to_job(self):
        """Assign a tag to a job application via JobApplication."""
        self.list_jobs()
        job_id = input("Enter job application ID: ").strip()
        self.list_tags()
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

    def remove_tag_from_job(self):
        """Remove a tag from a job application."""
        self.list_jobs()
        job_id = input("Enter job application ID: ").strip()
        self.list_tags()
        tag_id = input("Enter tag ID: ").strip()
        
        try:
            job_id, tag_id = int(job_id), int(tag_id)
            JobApplicationTag.delete_tag_from_job(job_id, tag_id)
            print(f"Tag {tag_id} removed from job {job_id}.")
        except ValueError:
            print("Invalid input. Please enter valid numerical IDs.")

    def list_jobs(self):
        """List all job applications as a table."""
        jobs = JobApplication.get_all()

        if not jobs:
            print("No job applications found.")
        else:
            table = Table(title="Job Applications", show_header=True, header_style="bold cyan")
            table.add_column("Job ID", style="bold yellow")
            table.add_column("Job Title", style="white")
            table.add_column("Status", style="green")

            for job in jobs:
                table.add_row(str(job.id), job.job_title, job.status)

            self.console.print(table)

    def create_job(self):
        """Prompt the user to create a new job application."""
        job_title = input("Enter job title: ").strip().capitalize()
        
        company_name = input("Enter company name: ").strip().capitalize()
        
        company = Company.find_by_name(company_name)
        
        if not company:
            print(f"No company found with the name '{company_name}'")
            question = input("Would you like to create a company? (Y/N)").strip()
            if question.upper() == "Y":
                website = input("Enter company website: ").strip().lower()
                contact_info = input("Enter company contact info: ").strip().lower()
                company = Company(name=company_name, website=website or None, contact_info=contact_info or None)
                company.save()
                print(f"{company.name} created successfully!")
            else:
                return
        
        description = input("Enter job description: ").strip().lower()
        date_applied = self.helpers.get_valid_date("Enter date applied (YYYY-MM-DD): ")
        if not date_applied:
            return
            
        last_follow_up = self.helpers.get_valid_date(
            "Enter last follow-up date (YYYY-MM-DD or leave blank): ", 
            required=False, 
            must_be_after=date_applied
        )

        valid_statuses = ["applied", "pending", "rejected", "offer"]
        status = input("Enter job status (applied, pending, rejected, offer): ").strip().lower()
        
        while status not in valid_statuses:
            print("Invalid status. Please enter one of the following: applied, pending, rejected, offer.")
            status = input("Enter job status (applied, pending, rejected, offer): ").strip().lower()

        try:
            job = JobApplication(
                job_title=job_title,
                company_id=company.id,
                description=description,
                date_applied=date_applied,
                last_follow_up=last_follow_up,
                status=status
            )
            job.save()
            print(f"Job application '{job_title}' created successfully!")
        except ValueError as e:
            print(f"Error: {e}")

    def update_job(self):
        """Prompt the user to update an existing job application."""
        self.list_jobs()
        job_id = input("Enter job application ID to update: ").strip()

        try:
            job_id = int(job_id)
            job = JobApplication.find_by_id(job_id)
            
            if not job:
                print(f"Job application with ID {job_id} not found.")
                return

            print(f"Updating job application: {job.job_title} at Company ID {job.company_id}")

            job_title = input(f"Enter new job title (current: {job.job_title}): ").strip().capitalize()
            company_name = input(f"Enter new company name (current: {job.company_id}): ").strip().capitalize()

            company = Company.find_by_name(company_name) if company_name else None

            if company_name and not company:
                print(f"No company found with the name '{company_name}'. Please ensure the company exists.")
                return

            description = input(f"Enter new job description (current: {job.description}): ").strip().lower()
            
            date_applied = self.helpers.get_valid_date(
                f"Enter new date applied (current: {job.date_applied}, leave blank to keep current): ", 
                required=False
            )
            
            last_follow_up = self.helpers.get_valid_date(
                f"Enter new last follow-up date (current: {job.last_follow_up}, leave blank to keep current): ", 
                required=False,
                must_be_after=date_applied or job.date_applied
            )
            
            status = input(f"Enter new status (current: {job.status}): ").strip().lower()

            try:
                job.job_title = job_title if job_title else job.job_title
                job.company_id = company.id if company else job.company_id
                job.description = description if description else job.description
                job.date_applied = date_applied if date_applied else job.date_applied
                job.last_follow_up = last_follow_up if last_follow_up is not None else job.last_follow_up
                job.status = status if status else job.status

                job.update()
                print(f"Job application with ID {job_id} updated successfully.")
            except ValueError as e:
                print(f"Error: {e}")
        except ValueError:
            print("Invalid input. Please enter a valid job application ID.")

    def delete_job(self):
        """Prompt the user to delete a job application."""
        self.list_jobs()
        job_id = input("Enter job application ID to delete: ").strip()
        try:
            job_id = int(job_id)
            job = JobApplication.find_by_id(job_id)
            if job:
                job.delete()
                print(f"Job application ID {job_id} deleted successfully.")
            else:
                print(f"Job application ID {job_id} not found.")
        except ValueError:
            print("Invalid input. Please enter a valid job ID.")

    def list_companies(self):
        """List all companies as a table."""
        companies = Company.get_all()

        if not companies:
            print("No companies found.")
        else:
            table = Table(title="Companies", show_header=True, header_style="bold cyan")
            table.add_column("Company ID", style="bold yellow")
            table.add_column("Company Name", style="white")
            table.add_column("Website", style="white")
            table.add_column("Contact Info", style="white")

            for company in companies:
                table.add_row(
                    str(company.id), 
                    company.name, 
                    company.website or "-", 
                    company.contact_info or "-"
                )

            self.console.print(table)

    def create_company(self):
        """Prompt user to create new company"""
        name = input("Enter company name: ").strip().capitalize()
        website = input("Enter company website: ").strip().lower()
        contact_info = input("Enter company contact info: ").strip().lower()

        company = Company(name=name, website=website or None, contact_info=contact_info or None)
        company.save()
        print(f"{company.name} created successfully!")

    def update_company(self):
        """Prompt the user to update a company."""
        self.list_companies()
        company_id = input("Enter the company ID you want to update: ").strip()

        try:
            company_id = int(company_id)
            company = Company.find_by_id(company_id)
            if not company:
                print(f"Company with ID: {company_id} not found.")
                return
                
            print(f"Updating company: {company.name}")
            name = input(f"Enter new name (current: {company.name}): ").strip().capitalize()
            website = input(f"Enter new website (current: {company.website}): ").strip().lower()
            contact_info = input(f"Enter new contact info (current: {company.contact_info}): ").strip().lower()

            company.name = name if name else company.name
            company.website = website if website else company.website
            company.contact_info = contact_info if contact_info else company.contact_info
            
            company.update()
            print(f"Company with ID {company_id} updated successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid company ID.")

    def delete_company(self):
        """Prompt the user to delete a company."""
        self.list_companies()
        company_id = input("Enter the company ID to delete: ").strip()
        
        try:
            company_id = int(company_id)

            company = Company.find_by_id(company_id)
            
            if isinstance(company, Company):
                company.delete()
                print(f"Company with ID {company_id} ({company.name}) deleted successfully.")
            elif company is None:
                print(f"Company with ID {company_id} not found.")
            else:
                print(f"Error: {company}")
        except ValueError:
            print("Invalid input. Please enter a valid company ID.")

    def list_jobs_by_tag(self):
        """List all job applications associated with a specific tag."""
        self.list_tags()
        tag_id = input("Enter tag ID to list jobs: ").strip()

        try:
            tag_id = int(tag_id)
            tag = Tag.find_by_id(tag_id)
            jobs = tag.job_applications()

            if not jobs:
                print("No job applications found with this tag.")
            else:
                print(f"Job Applications with Tag ID {tag_id}:")
                for job in jobs:
                    print(f"  {job.id}: {job.job_title}")
        except ValueError:
            print("Invalid input. Please enter a valid tag ID.")