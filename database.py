import sqlite3
from dataclasses import dataclass

class Database():

    def __init__(self, banco) -> None:
        self.conn = sqlite3.connect(banco + ".db")

        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL);")

    def add(self, note):
        self.cursor.execute(f"INSERT INTO note (title,content) VALUES ('{note.title}','{note.content}');")
        self.conn.commit()

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''