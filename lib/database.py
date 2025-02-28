import sqlite3


class Database:
    def __init__(self, db_name="database.db"):
        """Initialize the database connection."""
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def execute(self, query, params=()):
        """Execute a query with optional parameters."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch(self, query, params=()):
        """Fetch results from a query."""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.connection.close()