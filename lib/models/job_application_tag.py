from lib.models.tag import Tag
from models import CONN, CURSOR
import sqlite3


#! _______ JOIN TABLE ___________
# foreign key as primary keys

class JobApplicationTag:
    def __init__(self, tag_id, post_id, id=None):
        self.id = id
        self.tag_id = tag_id
        self.post_id = post_id

    @classmethod
    def create_table(cls):
        """Create the post_tags table."""
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS job_application_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES job_applications(id) ON DELETE CASCADE,
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
            INSERT INTO post_tags (post_id, tag_id)
            VALUES (?, ?)
            """, (self.post_id, self.tag_id))
            CONN.commit()
            self.id = CURSOR.lastrowid 
            print(f"Post-tag relationship saved successfully with ID {self.id}.")
        except sqlite3.IntegrityError as e:
            print(f"Integrity error occurred while saving post-tag relationship: {e}")
        except sqlite3.Error as e:
            print(f"An error occurred while saving post-tag relationship: {e}")
        

    @classmethod
    def get_all(cls):
        """Retrieve all post-tag relationships."""
        try:
            CURSOR.execute("SELECT * FROM post_tags")
            rows = CURSOR.fetchall()
            return [cls(id=row[0], post_id=row[1], tag_id=row[2]) for row in rows]
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
    def get_tags_for_job(cls, job_id):
        """Retrieve all tags linked to a job."""
        CURSOR.execute("""
        SELECT tags.id, tags.name, tags.tag_type 
        FROM job_application_tags
        JOIN tags ON job_application_tags.tag_id = tags.id
        WHERE job_application_tags.post_id = ?
        """, (job_id,))
    
        return [Tag(id=row[0], name=row[1], tag_type=row[2]) for row in CURSOR.fetchall()]

    @classmethod
    def get_jobs_by_tag(cls, tag_id):
        """Retrieve all jobs linked to a tag."""
        CURSOR.execute("""
        SELECT job_applications.id, job_applications.job_title 
        FROM job_application_tags
        JOIN job_applications ON job_application_tags.post_id = job_applications.id
        WHERE job_application_tags.tag_id = ?
        """, (tag_id,))
    
        return CURSOR.fetchall()
    
    @classmethod
    def delete_tag_from_job(cls, job_id, tag_id):
        """Remove a specific tag from a job application."""
        CURSOR.execute("DELETE FROM job_application_tags WHERE post_id = ? AND tag_id = ?", (job_id, tag_id))
        CONN.commit()
