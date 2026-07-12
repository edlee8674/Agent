import sqlite3
import json


class EmbeddingCache:

    def __init__(self, db_path="embedding_cache.db"):

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS embedding_cache(
            text TEXT PRIMARY KEY,
            embedding TEXT
        )
        """)

        self.conn.commit()
    def get(self, text: str):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT embedding
            FROM embedding_cache
            WHERE text=?
            """,
            (text,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return json.loads(row[0])

    def save(self, text: str, embedding):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE
            INTO embedding_cache(text, embedding)
            VALUES (?, ?)
            """,
            (
                text,
                json.dumps(embedding)
            )
        )

        self.conn.commit()

