# lib/cli.py
from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag
from helpers import exit_program

def main():
    while True:
        menu()
        choice = input("> ")
        
        if choice == "0":
            exit_program()
        elif choice == "1":
            list_tags()
        elif choice == "2":
            create_tag()
        elif choice == "3":
            delete_tag()
        elif choice == "4":
            assign_tag_to_job()
        elif choice == "5":
            remove_tag_from_job()
        elif choice == "6":
            list_jobs_by_tag()
        else:
            print("Invalid choice. Please try again.")

def menu():
    print("\n--- Job Application CLI ---")
    print("0. Exit the program")
    print("1. List all tags")
    print("2. Create a new tag")
    print("3. Delete a tag")
    print("4. Assign a tag to a job")
    print("5. Remove a tag from a job")
    print("6. List jobs by a tag")

def list_tags():
    """List all available tags."""
    tags = Tag.get_all()
    if not tags:
        print("No tags found.")
    else:
        for tag in tags:
            print(f"{tag.id}: {tag.name} ({tag.tag_type})")

def create_tag():
    """Create a new tag."""
    name = input("Enter tag name: ").strip()
    tag_type = input("Enter tag type (location/length): ").strip().lower()
    
    if tag_type not in ["location", "length"]:
        print("Invalid tag type. Must be 'location' or 'length'.")
        return

    tag = Tag(name=name, tag_type=tag_type)
    tag.save()
    print(f"Tag '{name}' added successfully.")

def delete_tag():
    """Delete a tag."""
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
            for job in jobs:
                print(f"Job {job[0]}: {job[1]}")
    except ValueError:
        print("Invalid input. Please enter a valid tag ID.")

if __name__ == "__main__":
    main()
