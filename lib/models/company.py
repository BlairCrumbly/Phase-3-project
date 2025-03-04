from models import CONN, CURSOR
import sqlite3

class Company:
    def __init__(self, name, website, contact_info, id=None):
        self.id = id
        self.name = name
        self.website = website
        self.contact_info = contact_info


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Company name must be a non-empty string.")
        self._name = value.strip()

    @property
    def website(self):
        return self._website

    @website.setter
    def website(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Website must be a string or None.")
        self._website = value

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value):
        if value is not None and not isinstance(value, str):
            raise TypeError("Contact info must be a string or None.")
        self._contact_info = value

    @classmethod
    def create_table(cls):
        try:
            CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL CHECK(LENGTH(name) > 0),
                website TEXT,
                contact_info TEXT
            )
            """)
            CONN.commit()
            print("Table 'companies' created successfully.")
        except sqlite3.Error as e:
            print(f"An error occurred while creating the table: {e}")
    
    @classmethod
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

    
    @classmethod
    def find_by_id(cls, id):
        """Find a company by ID."""
        CURSOR.execute("SELECT * FROM companies WHERE id = ?", (id,))
        row = CURSOR.fetchone()
        return cls(id=row[0], name=row[1], website=row[2], contact_info=row[3]) if row else None


    @classmethod
    def find_by_name(cls, name):
        """Find a company by its name."""
        CURSOR.execute("SELECT * FROM companies WHERE name = ?", (name,))
        row = CURSOR.fetchone()
        if row:
            return cls(*row) 
        return None