from models import CONN, CURSOR
import sqlite3

class Tag:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    @classmethod
    def create_table(cls):
        """Create the tags table."""
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
                length_name TEXT CHECK(length_name IN ('full-time','part-time')),
                location_name TEXT CHECK(location_name IN ('remote','hybrid','in-person'))
            )
            """)
            print("Table 'tags' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")

    def save(self):
        """Save a new tag to the database."""
        CURSOR.execute("INSERT INTO tags (name) VALUES (?)", (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid  # Set the object's ID after insertion

    @classmethod
    def get_all(cls):
        """Retrieve all tags from the database."""
        CURSOR.execute("SELECT * FROM tags")
        return [cls(id=row[0], name=row[1]) for row in CURSOR.fetchall()]

    @classmethod
    def drop_table(cls):
        """Drop the tags table."""
        try:
            CURSOR.execute("DROP TABLE IF EXISTS tags")
            CONN.commit()
            print("Table 'tags' dropped successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping the table: {e}")