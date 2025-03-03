from models import CONN, CURSOR
import sqlite3

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
