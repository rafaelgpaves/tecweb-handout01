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

    def get_all(self):
        cursor = self.cursor.execute("SELECT id, title, content FROM note;")
        notes = []
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            notes.append(Note(id=id, title=title, content=content))
        return notes
    
    def update(self, entry):
        self.cursor.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}' WHERE id = {entry.id};")
        self.conn.commit()

    def delete(self, note_id):
        self.cursor.execute(f"DELETE FROM note WHERE id = {note_id};")

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''