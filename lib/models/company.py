from models import CONN, CURSOR
import sqlite3

class Company:
    def __init__(self, name, website, contact_info, id=None):
        self.id = id
        self.name = name
        self.website = website
        self.contact_info = contact_info

    @classmethod
    def create_table(cls):
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(LENGTH(name) > 0),
                website TEXT,
                contact_info TEXT
            )
            """)
            CONN.commit()
            print("Table 'companies' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")
    
    def get_all(cls):
        """Retrieve all companies from the database."""
        try:
            CURSOR.execute("SELECT * FROM companies")
            return [cls(id=row[0], name=row[1], website=row[2], contact_info=row[3]) for row in CURSOR.fetchall()]
        except sqlite3.Error as e:
            print(f"An error occurred while retrieving companies: {e}")
            return []

    def save(self):
        """Save a new company to the database."""
        try:
            CURSOR.execute("INSERT INTO companies (name, website, contact_info) VALUES (?, ?, ?)",
                           (self.name, self.website, self.contact_info))
            CONN.commit()
            self.id = CURSOR.lastrowid  # Set the object's ID after insertion
            print(f"Company '{self.name}' saved successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while saving the company: {e}")
            
    @classmethod
    def drop_table(cls):
        """Drop the companies table."""
        try:
            CURSOR.execute("DROP TABLE IF EXISTS companies")
            CONN.commit()
            print("Table 'companies' dropped successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while dropping the table: {e}")