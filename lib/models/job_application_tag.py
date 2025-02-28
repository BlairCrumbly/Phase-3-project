from models import CONN, CURSOR

#! _______ JOIN TABLE ___________

class PostTag:
    def __init__(self, tag_id, post_id, id=None):
        self.id = id
        self.tag_id = tag_id
        self.post_id = post_id

    @classmethod
    def create_table(cls):
        """Create the post_tags table."""
        CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS post_tags (
            post_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY (post_id) REFERENCES posts(post_id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(tag_id) ON DELETE CASCADE
        )
        """)
        CONN.commit()

    def save(self):
        """Save a new post-tag relationship."""
        CURSOR.execute("INSERT INTO post_tags (post_id, tag_id) VALUES (?, ?)", (self.post_id, self.tag_id))
        CONN.commit()

    @classmethod
    def get_all(cls):
        """Retrieve all post-tag relationships."""
        CURSOR.execute("SELECT * FROM post_tags")
        return [cls(id=row[0], post_id=row[1], tag_id=row[2]) for row in CURSOR.fetchall()]
