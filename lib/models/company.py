from models import CONN, CURSOR
import sqlite3
from job_application import JobApplication

class Company:
    def __init__(self, name, website=None, contact_info=None, id=None):
        self.id = id
        self.name = name
        self.website = website
        self.contact_info = contact_info

#! props and validation
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Company name must be a non-empty string.")
        self._name = value.strip()

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Website must be a string or None.")
        self._website = value

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Contact info must be a string or None.")
        self._contact_info = value

    @classmethod
    def create_table(cls):
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(LENGTH(name) > 0),
                website TEXT,
                contact_info TEXT
            )
            """)

            return ("Table 'companies' created successfully.")
        except sqlite3.Error as e:
            return (f"An error occurred while creating the table: {e}")
    #! retrieve all companies from the database
    @classmethod
    def get_all(cls):
        """Retrieve all companies from the database."""
        try:
            CURSOR.execute("SELECT * FROM companies")
            return [cls(id=row[0], name=row[1], website=row[2], contact_info=row[3]) for row in CURSOR.fetchall()]
        except sqlite3.Error as e: 
            return(f"An error occurred while retrieving companies: {e}")
            
        except Exception as e: # the most general 
            return e
        #add another except 
    #! find company by name
    @classmethod
    def find_by_name(cls, name):
        """Find a company by name."""
        try: #!how you can do if in SQL , any condition
            CURSOR.execute("SELECT * FROM companies WHERE name = ?", (name,))
            row = CURSOR.fetchone()
            if row:
                return cls(id=row[0], name=row[1], website=row[2], contact_info=row[3])

        except sqlite3.Error as e:
            return(f"An error occurred while finding the company: {e}")
            # add drop 


    #! find company by ID
    @classmethod
    def find_by_id(cls, company_id):
        """Find a company by ID."""
        try:
            CURSOR.execute("SELECT company_id, name, website, contact_info FROM companies WHERE company_id = ?", (company_id,))
            row = CURSOR.fetchone()
            if row:
                return cls(id=row[0], name=row[1], website=row[2], contact_info=row[3])

        except sqlite3.Error as e:
            return(f"An error occurred while finding the company: {e}")


    #! count total number of companies
    @classmethod
    def count(cls):
        try:
            CURSOR.execute("SELECT COUNT(*) FROM companies")
            return CURSOR.fetchone()[0]
        except sqlite3.Error as e:
            return(f"An error occurred while counting companies: {e}")



#! save a new company to the db
    def save(self):
        """Save a new company to the database."""
        try:
            CURSOR.execute("INSERT INTO companies (name, website, contact_info) VALUES (?, ?, ?)",
            (self.name, self.website, self.contact_info))
            CONN.commit()
            self.id = CURSOR.lastrowid  #! set the object's ID after insertion to match the database record
            return self
        except sqlite3.Error as e:
            CONN.rollback() # add to every changing method
            return(f"An error occurred while saving the company: {e}")

     #! uppdate an existing company
    def update(self):
        if self.id is None:
            print("Company must have an ID before updating.")
            return
        try:
            CURSOR.execute("UPDATE companies SET name = ?, website = ?, contact_info = ? WHERE company_id = ?",
                           (self.name, self.website, self.contact_info, self.id))
            CONN.commit()
            return(f"Company '{self.name}' updated successfully.")
        except sqlite3.Error as e:
            CONN.rollback()
            return(f"An error occurred while updating the company: {e}")
        
    @classmethod
    def find_top_two_companies(cls):
         
        try:
            CURSOR.execute("""
                SELECT company_id
                FROM job_applications
                JOIN companies ON job_applications.company_id = companies.id
                GROUP BY company_id
                ORDER BY COUNT(*) DESC
                LIMIT 2
            """)
            rows = CURSOR.fetchall() #list of tuples

            return [{
                "company_id": row[0],
                "company_name": row[1],
            } for row in rows]
        
        except Exception as e:
            return e



#!association methods

#todo make method that fetches related JobApplication instances
#todo make add_job_application method to assocaite JobApplication instance with a company


def job_applications(self):
    """get all columns from job_applications that match the id of the company instance and filter rows
    where the company.id matches the given value
    """
    try:
        CURSOR.execute("SELECT * FROM job_applications WHERE company.id = ?",  self.id)
        job_applications = CURSOR.fetchall()
        return [JobApplication(*row) for row in job_applications]
    except sqlite3.Error as e:
        return f"An error occurred while retrieving job applications for company {e}"


def add_job_application(self, job_application):

    if not isinstance(job_application, JobApplication):
        raise TypeError("Provided object must be a JobApplication instance")
    try:
        job_application.company_id = self.id #! make sure company id is  set
        job_application.save()
        return f"Job application '{job_application.job_title}' successfully associated with company '{self.name}'."
    except Exception as e:
        return f"An error occurred while associating the job application: {e}"


@classmethod
def drop_table(cls):
        #!drop the companies table.
    try:
        CURSOR.execute("DROP TABLE IF EXISTS companies")
        return("Table 'companies' dropped successfully.")
    except sqlite3.Error as e:
        return(f"An error occurred while dropping the table: {e}")







Company.create_table()
