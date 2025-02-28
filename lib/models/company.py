from models import CONN, CURSOR

class Company:
    def __init__(self, name, website, contact_info, id=None):
        self.id = id
        self.name = name
        self.website = website
        self.contact_info = contact_info

    @classmethod
    def create_table(cls):
        CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            website TEXT,
            contact_info TEXT
        )
        """)
        CONN.commit()

    def save(self):
        CURSOR.execute("INSERT INTO companies (name, website, contact_info) VALUES (?, ?, ?)",
                       (self.name, self.website, self.contact_info))
        CONN.commit()
