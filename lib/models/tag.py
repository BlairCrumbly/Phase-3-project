from models import CONN, CURSOR
import sqlite3
import ipdb
from sqlite3 import IntegrityError


class Tag:
    VALID_TAG_TYPES = {"location", "length"}

    def __init__(self, name, tag_type, id=None):
        self.id = id
        self.name = name
        self.tag_type = tag_type


    def job_application_tags(self):
        try:
            from models.job_application_tag import JobApplicationTag
            CURSOR.execute("""
            SELECT * FROM job_application_tags WHERE tag_id == ?
            """, (self.id,))
            job_app_tags = CURSOR.fetchall()
            return [
                JobApplicationTag(id=job_app_tag[0], job_id=job_app_tag[1], tag_id=job_app_tag[2])
                for job_app_tag in job_app_tags
            ]
        except Exception as e:
            return(f"Error retrieving job applications for tag {self.id}: {e}")
    
    def job_applications(self):
        try:
            from models.job_application_tag import JobApplicationTag
            return [
                job_app_tag.job_application() for job_app_tag in self.job_application_tags()
            ]
        except Exception as e:
            return(f"Error retrieving job applications for tag {self.id}: {e}")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Tag name must be a non-empty string.")
        self._name = value.strip()

    @property
    def tag_type(self):
        return self._tag_type

    @tag_type.setter
    def tag_type(self, value):
        if value not in self.VALID_TAG_TYPES:
            raise ValueError(f"Invalid tag type. Must be one of {self.VALID_TAG_TYPES}")
        self._tag_type = value


    @classmethod
    def create_table(cls):
        """Create the tags table."""
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            tag_type TEXT CHECK(tag_type IN ('location', 'length')) NOT NULL
            )
            """)
            print("Table 'tags' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")   
            

    def save(self):
        """Save a new tag to the database."""
        try:
            CURSOR.execute("INSERT INTO tags (name, tag_type) VALUES (?, ?)", (self.name, self.tag_type))
            CONN.commit()
            self.id = CURSOR.lastrowid  # Set the object's ID after insertion
            print(f"Tag '{self.name}' saved successfully.")
        except IntegrityError as e:
            print("IntegrityError: {e} - This tag already exists or violates a database constraint.")
        

    @classmethod
    def get_all(cls):
        """Retrieve all tags from the database."""
        try:
            CURSOR.execute("SELECT * FROM tags")
            rows = CURSOR.fetchall()
            return [cls(id=row[0], name=row[1], tag_type=row[2]) for row in rows]
        except sqlite3.Error as e:
                print(f"An error occurred while retrieving tags: {e}")
                return []  # Return an empty list in case of an error

    @classmethod
    def drop_table(cls):
        """Drop the tags table."""
        try:
            CURSOR.execute("DROP TABLE IF EXISTS tags")
            CONN.commit()
            print("Table 'tags' dropped successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping the table: {e}")

    @classmethod
    def find_by_name(cls, name):
        """Find a tag by name."""
        CURSOR.execute("SELECT * FROM tags WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        return cls(id=row[0], name=row[1], tag_type=row[2]) if row else None

    @classmethod
    def delete(cls, id):
        """Delete a tag if it's not linked to any jobs."""
        try:
            CURSOR.execute("DELETE FROM tags WHERE id = ?", (id,))
            CONN.commit()
            print(f"Tag {id} deleted.")
        except sqlite3.Error as e:
            print(f"Error deleting tag: {e}")


    @classmethod
    def find_by_id(cls, id):
        """Find a tag by ID."""
        CURSOR.execute("SELECT * FROM tags WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls(id=row[0], name=row[1], tag_type=row[2]) if row else None

