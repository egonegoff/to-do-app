import sqlite3
from Todo_Data import TodoDataclass

class Todo_Service_Class:
    def __init__(self, db_path="todos.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("""
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    done INTEGER DEFAULT 0
                )
            """)
            conn.commit()

    def add_todo(self, text: str):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("INSERT INTO todos (text, done) VALUES (?, ?)", (text, 0))
            conn.commit()

    def get_all_todos(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("SELECT id, text, done FROM todos")
            rows = c.fetchall()
            return [TodoDataclass(id=row[0], text=row[1], done=bool(row[2])) for row in rows]

    def update_todo_status(self, todo_id: int, done: bool):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("UPDATE todos SET done=? WHERE id=?", (int(done), todo_id))
            conn.commit()

    def delete_todo(self, todo_id: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM todos WHERE id=?", (todo_id,))
            conn.commit()
