import sqlite3
from dataclasses import dataclass

class Database():

    def __init__(self, banco) -> None:
        self.conn = sqlite3.connect(banco + ".db")

        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL, color TEXT NOT NULL);")

    def add(self, note):
        self.cursor.execute(f"INSERT INTO note (title,content,color) VALUES ('{note.title}','{note.content}','{note.color}');")
        self.conn.commit()

    def get_id(self, id):
        cursor = ((self.cursor.execute(f"SELECT * FROM note WHERE id={id};")).fetchall())[0]
        print(cursor)
        return Note(id=id, title=cursor[1], content=cursor[2], color=cursor[3])

    def get_all(self):
        cursor = self.cursor.execute("SELECT id, title, content, color FROM note;")
        notes = []
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            color = linha[3]
            notes.append(Note(id=id, title=title, content=content, color=color))
        return notes
    
    def update(self, entry):
        self.cursor.execute(f"UPDATE note SET title = '{entry.title}', content = '{entry.content}', color = '{entry.color}' WHERE id = {entry.id};")
        self.conn.commit()

    def delete(self, note_id):
        self.cursor.execute(f"DELETE FROM note WHERE id = {note_id};")
        self.conn.commit()

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    color: str = ''