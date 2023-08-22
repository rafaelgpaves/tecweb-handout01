import sqlite3

class Database():

    def __init__(self, banco) -> None:
        self.conn = sqlite3.connect(banco + ".db")

        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS note ( id INTEGER PRIMARY KEY, title TEXT, content TEXT NOT NULL);")