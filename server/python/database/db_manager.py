import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        # DEV MODE → drop & recreate
        if os.getenv("FLASK_ENV") == "development":
            cursor.execute("DROP TABLE IF EXISTS tasks")
            
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                completed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

def load_tasks():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, description, due_date, priority, status, created_at, completed
            FROM tasks
        """)
        rows = cursor.fetchall()
        return [
            {
                "id": r[0],
                "title": r[1],
                "description": r[2],
                "dueDate": r[3],
                "priority": r[4],
                "status": r[5],
                "createdAt": r[6],
                "completed": bool(r[7]),
            }
            for r in rows
        ]

def add_task(title, description, due_date, priority, status):
    with get_connection() as conn:
        cursor = conn.cursor()
        completed = 1 if status == "completed" else 0
        cursor.execute(
            """
            INSERT INTO tasks (title, description, due_date, priority, status, completed)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (title, description, due_date, priority, status, completed),
        )
        conn.commit()
        return cursor.lastrowid

def update_task(task_id, title, description, due_date, priority, status):
    with get_connection() as conn:
        cursor = conn.cursor()
        completed = 1 if status == "completed" else 0
        cursor.execute(
            """
            UPDATE tasks
            SET title=?, description=?, due_date=?, priority=?, status=?, completed=?
            WHERE id=?
            """,
            (title, description, due_date, priority, status, completed, task_id),
        )
        conn.commit()
        return cursor.rowcount > 0

def delete_task(task_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        return cursor.rowcount > 0

def mark_task(task_id, completed: bool):
    with get_connection() as conn:
        cursor = conn.cursor()
        status = "completed" if completed else "pending"
        cursor.execute(
            "UPDATE tasks SET completed=?, status=? WHERE id=?",
            (1 if completed else 0, status, task_id),
        )
        conn.commit()
        return cursor.rowcount > 0