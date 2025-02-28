from models import CONN, CURSOR

class JobApplication:
    def __init__(self, job_title, company_id, description, date_applied, last_follow_up, status, id=None):
        self.id = id
        self.job_title = job_title
        self.company_id = company_id
        self.description = description
        self.date_applied = date_applied
        self.last_follow_up = last_follow_up
        self.status = status

    @classmethod
    def create_table(cls):
        """Create the job_applications table."""
        CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT NOT NULL,
            company_id INTEGER,
            description TEXT,
            date_applied DATE,
            last_follow_up DATE,
            status TEXT CHECK(status IN ('applied', 'pending', 'rejected', 'offer')),
            FOREIGN KEY (company_id) REFERENCES companies(company_id)
        )
        """)
        CONN.commit()

    def save(self):
        """Save a new job application to the database."""
        CURSOR.execute("""
        INSERT INTO job_applications (job_title, company_id, description, date_applied, last_follow_up, status)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (self.job_title, self.company_id, self.description, self.date_applied, self.last_follow_up, self.status))
        CONN.commit()
        self.id = CURSOR.lastrowid  # Set the object's ID after insertion
