from models import CONN, CURSOR

class Tag:
    def __init__(self, name, id=None):
        self.id = id
        self.name = name

    @classmethod
    def create_table(cls):
        """Create the tags table."""
        CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            tag_id INTEGER PRIMARY KEY AUTOINCREMENT,
            length_name TEXT CHECK(name IN ('full-time','part-time',))
            location_name TEXT CHECK(name IN ('remote','hybrid','in-person'))
        )
        """)

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

    #DROP TABLE