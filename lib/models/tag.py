from models import CONN, CURSOR
import sqlite3

class Tag:
    def __init__(self, name, tag_type, id=None):
        self.id = id
        self.name = name
        self.tag_type = tag_type  # Store the tag type ('location' or 'length')

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
        except sqlite3.Error as e:
            print(f"An error occurred while saving the tag: {e}")

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