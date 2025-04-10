import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from tkinter import StringVar

# Connect to SQLite
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        due_date TEXT,
        priority TEXT,
        status TEXT DEFAULT "Pending"
    )
''')
conn.commit()

# Functions
def add_task():
    title = title_var.get().strip()
    description = desc_var.get().strip()
    due_date = date_var.get().strip()
    priority = priority_var.get()

    if not title or not due_date:
        messagebox.showwarning("Missing Info", "Title and Due Date are required!")
        return

    cursor.execute("INSERT INTO tasks (title, description, due_date, priority) VALUES (?, ?, ?, ?)",
                   (title, description, due_date, priority))
    conn.commit()
    refresh_tasks()

def delete_task():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Select", "Please select a task to delete.")
        return

    task_id = tree.item(selected[0])["values"][0]
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    refresh_tasks()

def mark_complete():
    selected = tree.selection()
    if not selected:
        messagebox.showinfo("Select", "Please select a task to mark as complete.")
        return

    task_id = tree.item(selected[0])["values"][0]
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE id = ?", (task_id,))
    conn.commit()
    refresh_tasks()

def refresh_tasks():
    for item in tree.get_children():
        tree.delete(item)

    cursor.execute("SELECT * FROM tasks")
    for row in cursor.fetchall():
        status_style = "success" if row[5] == "Completed" else "warning"
        tree.insert("", END, values=row, tags=(status_style,))
    style_rows()

def style_rows():
    tree.tag_configure("success", background="#d4edda")
    tree.tag_configure("warning", background="#fff3cd")

# GUI Window
app = ttk.Window(themename="superhero")
app.title("Smart Task Manager")
app.geometry("900x500")
app.resizable(False, False)

# Variables
title_var = StringVar()
desc_var = StringVar()
date_var = StringVar()
priority_var = StringVar(value="Medium")

# Inputs
ttk.Label(app, text="Title:").place(x=20, y=15)
ttk.Entry(app, textvariable=title_var, width=30).place(x=80, y=15)

ttk.Label(app, text="Description:").place(x=20, y=45)
ttk.Entry(app, textvariable=desc_var, width=30).place(x=100, y=45)

ttk.Label(app, text="Due Date (YYYY-MM-DD):").place(x=400, y=15)
ttk.Entry(app, textvariable=date_var, width=20).place(x=580, y=15)

ttk.Label(app, text="Priority:").place(x=400, y=45)
ttk.Combobox(app, textvariable=priority_var, values=["Low", "Medium", "High"], width=17).place(x=470, y=45)

# Buttons
ttk.Button(app, text="Add Task", bootstyle="primary", command=add_task).place(x=150, y=90)
ttk.Button(app, text="Delete Task", bootstyle="danger", command=delete_task).place(x=270, y=90)
ttk.Button(app, text="Mark Complete", bootstyle="success", command=mark_complete).place(x=400, y=90)
ttk.Button(app, text="Refresh", bootstyle="info", command=refresh_tasks).place(x=550, y=90)

# Treeview for Task Table
cols = ("ID", "Title", "Description", "Due Date", "Priority", "Status")
tree = ttk.Treeview(app, columns=cols, show="headings", height=15, bootstyle="secondary")

for col in cols:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)

tree.place(x=20, y=140, width=860, height=330)
refresh_tasks()

app.mainloop()
