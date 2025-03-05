from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag


def create_tables():
    Company.create_table()
    JobApplication.create_table()
    Tag.create_table()
    JobApplicationTag.create_table()

def drop_tables():
    Tag.drop_table()
    JobApplicationTag.drop_table()
    Company.drop_table()
    JobApplication.drop_table()
    
def seed_data():
    """Seed the database with sample data."""
    # Seed Companies
    company1 = Company(name="TechCorp", website="https://techcorp.com", contact_info="contact@techcorp.com")
    company1.save()
    
    company2 = Company(name="WebWorks", website="https://webworks.com", contact_info="info@webworks.com")
    company2.save()

    company3 = Company(name="Noogle", website="https://webworks.com", contact_info="info@webworks.com")
    company3.save()

    # Seed Tags
    location_tag1 = Tag(name="remote", tag_type="location")
    location_tag1.save()

    location_tag2 = Tag(name="hybrid", tag_type="location")
    location_tag2.save() 

    length_tag1 = Tag(name="full-time", tag_type="length")
    length_tag1.save()

    length_tag2 = Tag(name="part-time", tag_type="length")
    length_tag2.save()

    # Seed Job Applications
    job_app1 = JobApplication(job_title="Software Engineer", company_id=company1.id, description="Develop software.", date_applied="2025-02-28", last_follow_up="2025-03-05", status="applied")
    job_app1.save()

    job_app2 = JobApplication(job_title="Web Developer", company_id=company2.id, description="Build websites.", date_applied="2025-02-20", last_follow_up="2025-02-25", status="pending")
    job_app2.save()

    job_app3 = JobApplication(job_title="Web Developer", company_id=company2.id, description="Build websites.", date_applied="2025-02-20", last_follow_up="2025-02-25", status="pending")
    job_app3.save()


    # Seed Job Application Tags
    # Ensure tag_id is valid (the tags must be saved first)
    job_app_tag1 = JobApplicationTag(tag_id=location_tag1.id, post_id=job_app1.id)
    job_app_tag1.save()

    job_app_tag2 = JobApplicationTag(tag_id=length_tag2.id, post_id=job_app2.id)
    job_app_tag2.save()



def test_data():
    """Test and display the data in the database."""
    # Test: Get all companies
    companies = Company.get_all()
    print("Companies:")
    for company in companies:
        print(f"ID: {company.id}, Name: {company.name}, Website: {company.website}, Contact: {company.contact_info}")

    # Test: Get all job applications
    # job_apps = JobApplication.get_all()
    # print("\nJob Applications:")
    # for job in job_apps:
    #     print(f"ID: {job.id}, Job Title: {job.job_title}, Status: {job.status}, Company ID: {job.company_id}")

    # Test: Get all tags
    tags = Tag.get_all()
    print("\nTags:")
    for tag in tags:
        print(f"ID: {tag.id}, Name: {tag.name}")

    # Test: Get all job application tags
    job_app_tags = JobApplicationTag.get_all()
    print("\nJob Application Tags:")
    for tag in job_app_tags:
        print(f"Job Application ID: {tag.post_id}, Tag ID: {tag.tag_id}")

if __name__ == "__main__":

    drop_tables()
    
    # Create tables
    create_tables()

    # Seed the database with data
    seed_data()

    # Test the data
    # test_data()

    # Optionally, you can drop tables if needed
    # drop_tables()

