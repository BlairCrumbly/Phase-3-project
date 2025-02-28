from models.company import Company
from models.job_application import JobApplication
from models.tag import Tag
from models.job_application_tag import JobApplicationTag

def create_tables():
    Company.create_table()
    JobApplication.create_table()
    Tag.create_table()
    JobApplicationTag.create_table()


#drop tables method
def drop_tables():
    Tag.drop_table()
    JobApplicationTag.drop_table()
    Company.drop_table()
    JobApplication.drop_table()
    
if __name__ == "__main__":
    create_tables()


