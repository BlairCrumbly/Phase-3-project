from models.tag import Tag
from models import CONN, CURSOR
import sqlite3
import ipdb


#! _______ JOIN TABLE ___________

class JobApplicationTag:

    def __init__(self, tag_id, job_id, id=None):
        self.id = id
        self.tag_id = tag_id
        self.job_id = job_id


    def job_application(self):
        try:
            return JobApplication.find_by_id(self.job_id)
        except Exception as e:
            print(f"Error retrieving job application for tag {self.id}: {e}")
            return None
            
    
    @property
    def tag_id(self):
        return self._tag_id

    @tag_id.setter
    def tag_id(self, value):
        if not isinstance(value, int) or not Tag.find_by_id(value):
            #separate errors
            raise ValueError(f"Invalid tag_id {value}. It must be an existing tag ID.")
        self._tag_id = value

    @property
    def job_id(self):
        return self._job_id

    @job_id.setter
    def job_id(self, value):
        if not isinstance(value, int) or value <= 0:
            #separate errors
            raise ValueError(f"Invalid job_id {value}. It must be a positive integer.")
        self._job_id = value

#edit down prints
    @classmethod
    #indexing foreign keys?
    def create_table(cls):
        """Create the post_tags table."""
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS job_application_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (job_id) REFERENCES job_applications(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
            """)
            print("Table 'job_application_tags' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def save(self):
        """Save a new post-tag relationship."""
        try:
            CURSOR.execute("""
            INSERT INTO job_application_tags (job_id, tag_id)
            VALUES (?, ?)
            """, (self.job_id, self.tag_id))
            CONN.commit()
            self.id = CURSOR.lastrowid 
            print(f"Post-tag relationship saved successfully with ID {self.id}.")
        except sqlite3.IntegrityError as e:
            print(f"Integrity error occurred while saving post-tag relationship: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while saving post-tag relationship: {e}")
        

    @classmethod
    def get_all(cls):
        """Retrieve all job application-tag relationships."""
        try:
            CURSOR.execute("SELECT * FROM job_application_tags")
            rows = CURSOR.fetchall()
            return [cls(id=row[0], job_id=row[1], tag_id=row[2]) for row in rows]
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving post-tag relationships: {e}")
            return []  # Return an empty list in case of an error

    
    
    @classmethod
    def drop_table(cls):
        """Drop the job_application_tags table."""
        try:
            CURSOR.execute("DROP TABLE IF EXISTS job_application_tags")
            CONN.commit()
            print("Table 'job_application_tags' dropped successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping the table: {e}")

    @classmethod
    def create(cls, job_id, tag_id):
        """Creates a job-tag association, ensuring it doesn’t already exist."""
        try:
            existing = CURSOR.execute(
                "SELECT id FROM job_application_tags WHERE job_id = ? AND tag_id = ?",
                (job_id, tag_id)
            ).fetchone()

            if existing:
                raise ValueError(f"Tag {tag_id} is already assigned to job {job_id}.")

            job_tag = cls(job_id=job_id, tag_id=tag_id)
            job_tag.save()
            return job_tag
        except Exception as e:
            print(f"Database error: {e}")

    @classmethod
    def delete_tag_from_job(cls, job_id, tag_id):
        """Removes a tag from a job application."""
        try:
            CURSOR.execute(
                "DELETE FROM job_application_tags WHERE job_id = ? AND tag_id = ?",
                (job_id, tag_id)
            )
            CONN.commit()
            print(f"Tag {tag_id} removed from job {job_id}.")
        except Exception as e:
            print(f"Error removing tag: {e}")