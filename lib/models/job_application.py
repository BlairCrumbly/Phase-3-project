from models import CONN, CURSOR
from models.company import Company
from models.job_application_tag import JobApplicationTag
import sqlite3
import ipdb
from datetime import datetime

class JobApplication:
    VALID_STATUSES = {'applied', 'pending', 'rejected', 'offer'}

    def __init__(self, job_title, company_id, description, date_applied, last_follow_up, status, id=None):
        self.id = id
        self.job_title = job_title
        self.company_id = company_id
        self.description = description
        self.date_applied = date_applied
        self.last_follow_up = last_follow_up
        self.status = status

#association methods
    def job_application_tags(self):
        """Retrieve tags associated with the job application."""
        try:
            CURSOR.execute("""
            SELECT * FROM job_application_tags WHERE job_id = ? 
            """, (self.id,))
            job_tags = CURSOR.fetchall()
            return [JobApplicationTag(tag_id=job_tag[2], job_id=job_tag[1], id=job_tag[0]) for job_tag in job_tags]
        except sqlite3.Error as e:
            raise ValueError(f"Database error while fetching job application tags: {e}")
            return []

        
    
    def add_tag(self, tag_id):
        """Associates the job with a tag and handles errors."""
        try:
            from models.job_application_tag import JobApplicationTag

            JobApplicationTag.create(self.id, tag_id)
            print(f"Tag {tag_id} successfully assigned to job {self.id}.")
        except ValueError as e:
            print(f"Error: {e}")


    @property
    def company_id(self):
        return self._company_id

    @company_id.setter
    def company_id(self, value):
        if value is not None:
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"Invalid company_id {value}. It must be a positive integer or None.")
            if not Company.find_by_id(value):  # Check if company exists in DB
                raise ValueError(f"Company with ID {value} does not exist.")
            self._company_id = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status '{value}'. Must be one of {self.VALID_STATUSES}.")
        self._status = value

    @property
    def date_applied(self):
        return self._date_applied

    @date_applied.setter
    def date_applied(self, value):
        if not self._validate_date(value):
            raise ValueError(f"Invalid date format: {value}. Use YYYY-MM-DD.")
        self._date_applied = value

    @property
    def last_follow_up(self):
        return self._last_follow_up

    @last_follow_up.setter
    def last_follow_up(self, value):
        if value is not None and not self._validate_date(value):
            raise ValueError(f"Invalid date format: {value}. Use YYYY-MM-DD or leave empty.")
        self._last_follow_up = value

    def _validate_date(self, date):
        """Check if the date is in YYYY-MM-DD format and valid."""
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    

    @classmethod
    def create_table(cls):
        """Create the job_applications table."""
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS job_applications (
                job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT NOT NULL,
                company_id INTEGER,
                description TEXT,
                date_applied DATE,
                last_follow_up DATE,
                status TEXT CHECK(status IN ('applied', 'pending', 'rejected', 'offer')),
                FOREIGN KEY (company_id) REFERENCES companies(company_id) ON DELETE cascade
            )
            """)
            CONN.commit()
            print("Table 'job_applications' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")


    def save(self):
        """Save a new job application to the database."""
        try:
            CURSOR.execute("""
            INSERT INTO job_applications (job_title, company_id, description, date_applied, last_follow_up, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (self.job_title, self.company_id, self.description, self.date_applied, self.last_follow_up, self.status))
            CONN.commit()  
            self.id = CURSOR.lastrowid
            print(f"Job application '{self.job_title}' saved successfully with ID {self.id}.")
        except sqlite3.IntegrityError as e:
            print(f"Integrity error occurred while saving job application: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while saving job application: {e}")

    
    @classmethod
    def drop_table(cls):
        """Drop the job_applications table."""
        try:
            CURSOR.execute("DROP TABLE IF EXISTS job_applications")
            CONN.commit()
            print("Table 'job_applications' dropped successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping the table: {e}")

            
    @classmethod
    def find_by_id(cls, job_id):
        """Retrieve a job application by ID."""
        try:
            CURSOR.execute("SELECT * FROM job_applications WHERE job_id = ?", (job_id,))
            row = CURSOR.fetchone()
            if row is None:
                return None
            return cls(job_title=row[1], company_id=row[2], description=row[3], 
                   date_applied=row[4], last_follow_up=row[5], status=row[6], id=row[0])
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving job application ID {job_id}: {e}")
            return None

    @classmethod
    def get_all(cls):
        """Fetch all job applications."""
        try:
            CURSOR.execute("SELECT id, job_title, status, company_id FROM job_applications")
            rows = CURSOR.fetchall()
            return [cls(*row) for row in rows] if rows else []
        except sqlite3.Error as e:
            print(f"An error occurred while fetching all job applications: {e}")
            return []

#use kwargs!!!
    def update(self, **kwargs):
        """Update job application fields dynamically."""
        valid_fields = {'job_title', 'company_id', 'description', 'date_applied', 'last_follow_up', 'status'}
        updates = {key: value for key, value in kwargs.items() if key in valid_fields}
        
        if not updates:
            raise ValueError("No valid fields provided for update.")

        set_clause = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [self.id]

        try:
            CURSOR.execute(f"UPDATE job_applications SET {set_clause} WHERE job_id = ?", values)
            CONN.commit()
            
            for key, value in updates.items():
                setattr(self, key, value)

            print(f"Job application ID {self.id} updated successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while updating job application ID {self.id}: {e}")

    def delete(self):
        """Delete a job application."""
        try:
            CURSOR.execute("DELETE FROM job_applications WHERE job_id = ?", (self.id,))
            CONN.commit()
            print(f"Job application ID {self.id} deleted successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while deleting job application ID {self.id}: {e}")