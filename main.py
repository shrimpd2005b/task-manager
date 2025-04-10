import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# Database Setup
def init_db():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    priority TEXT,
                    status TEXT DEFAULT 'Pending')''')
    conn.commit()
    conn.close()

# Task Manager Class
class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Task Manager")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))

        self.create_widgets()
        self.display_tasks()

    def create_widgets(self):
        # Entry Frame
        frame = tk.Frame(self.root, padx=10, pady=10)
        frame.pack(fill=tk.X)

        tk.Label(frame, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.title_entry = tk.Entry(frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.desc_entry = tk.Entry(frame, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Due Date (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.due_entry = tk.Entry(frame, width=20)
        self.due_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame, text="Priority:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.priority_combo = ttk.Combobox(frame, values=["Low", "Medium", "High"], state="readonly", width=18)
        self.priority_combo.grid(row=1, column=3, padx=5, pady=5)
        self.priority_combo.set("Medium")

        # Button Frame
        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()

        tk.Button(btn_frame, text="Add Task", width=15, command=self.add_task).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete Task", width=15, command=self.delete_task).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Mark Complete", width=15, command=self.mark_complete).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Refresh", width=15, command=self.display_tasks).pack(side=tk.LEFT, padx=10)

        # Task Display
        self.tree = ttk.Treeview(self.root, columns=("ID", "Title", "Due", "Priority", "Status"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Due", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Status", text="Status")

        self.tree.column("ID", width=50)
        self.tree.column("Title", width=300)
        self.tree.column("Due", width=150)
        self.tree.column("Priority", width=100)
        self.tree.column("Status", width=100)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def add_task(self):
        title = self.title_entry.get()
        desc = self.desc_entry.get()
        due = self.due_entry.get()
        priority = self.priority_combo.get()

        if not title or not due:
            messagebox.showerror("Error", "Title and Due Date are required!")
            return

        try:
            datetime.strptime(due, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (title, description, due_date, priority) VALUES (?, ?, ?, ?)",
                  (title, desc, due, priority))
        conn.commit()
        conn.close()
        self.display_tasks()
        self.clear_entries()

    def delete_task(self):
        selected = self.tree.selection()
        if not selected:
            return

        task_id = self.tree.item(selected[0])['values'][0]
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        self.display_tasks()

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            return

        task_id = self.tree.item(selected[0])['values'][0]
        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task_id,))
        conn.commit()
        conn.close()
        self.display_tasks()

    def display_tasks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect('tasks.db')
        c = conn.cursor()
        c.execute("SELECT id, title, due_date, priority, status FROM tasks")
        rows = c.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert('', 'end', values=row)

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.priority_combo.set("Medium")

if __name__ == '__main__':
    init_db()
    root = tk.Tk()
    app = TaskManager(root)
    root.mainloop()
