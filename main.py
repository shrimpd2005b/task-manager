import tkinter as tk
from tkinter import messagebox, ttk
from database import connect_db, insert_task, view_tasks, delete_task, update_task

connect_db()

root = tk.Tk()
root.title("Smart Task Manager")
root.geometry("700x500")
root.config(bg="#f0f0f0")

# -------- Input Frame --------
frame_input = tk.Frame(root, bg="#ffffff", pady=10, padx=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="Title:").grid(row=0, column=0)
entry_title = tk.Entry(frame_input, width=40)
entry_title.grid(row=0, column=1)

tk.Label(frame_input, text="Description:").grid(row=1, column=0)
entry_desc = tk.Entry(frame_input, width=40)
entry_desc.grid(row=1, column=1)

tk.Label(frame_input, text="Due Date:").grid(row=2, column=0)
entry_date = tk.Entry(frame_input, width=40)
entry_date.grid(row=2, column=1)

tk.Label(frame_input, text="Priority:").grid(row=3, column=0)
priority_var = tk.StringVar()
priority_menu = ttk.Combobox(frame_input, textvariable=priority_var, values=["High", "Medium", "Low"])
priority_menu.grid(row=3, column=1)
priority_menu.current(1)

def add_task():
    title = entry_title.get()
    desc = entry_desc.get()
    date = entry_date.get()
    priority = priority_var.get()
    if title == "":
        messagebox.showwarning("Input Error", "Title is required!")
        return
    insert_task(title, desc, date, priority)
    entry_title.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    entry_date.delete(0, tk.END)
    priority_menu.current(1)
    show_tasks()

# -------- Task List --------
frame_list = tk.Frame(root)
frame_list.pack(fill="both", expand=True, pady=10)

task_tree = ttk.Treeview(frame_list, columns=("ID", "Title", "Due Date", "Priority", "Status"), show="headings")
task_tree.heading("ID", text="ID")
task_tree.heading("Title", text="Title")
task_tree.heading("Due Date", text="Due Date")
task_tree.heading("Priority", text="Priority")
task_tree.heading("Status", text="Status")
task_tree.pack(fill="both", expand=True)

def show_tasks():
    for i in task_tree.get_children():
        task_tree.delete(i)
    for row in view_tasks():
        task_tree.insert("", tk.END, values=row)

def delete_selected():
    selected = task_tree.selection()
    if selected:
        task_id = task_tree.item(selected[0])['values'][0]
        delete_task(task_id)
        show_tasks()

def mark_complete():
    selected = task_tree.selection()
    if selected:
        task_id = task_tree.item(selected[0])['values'][0]
        update_task(task_id, "Complete")
        show_tasks()

# -------- Buttons --------
frame_btns = tk.Frame(root, pady=10)
frame_btns.pack()

tk.Button(frame_btns, text="Add Task", command=add_task).pack(side="left", padx=10)
tk.Button(frame_btns, text="Delete Task", command=delete_selected).pack(side="left", padx=10)
tk.Button(frame_btns, text="Mark Complete", command=mark_complete).pack(side="left", padx=10)
tk.Button(frame_btns, text="Refresh", command=show_tasks).pack(side="left", padx=10)

show_tasks()
root.mainloop()

