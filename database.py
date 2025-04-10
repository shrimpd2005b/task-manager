import sqlite3

def connect_db():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        priority TEXT,
        status TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_task(title, description, due_date, priority):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?, ?)", 
                (title, description, due_date, priority, "Incomplete"))
    conn.commit()
    conn.close()

def view_tasks():
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

def update_task(task_id, status):
    conn = sqlite3.connect("tasks.db")
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()

