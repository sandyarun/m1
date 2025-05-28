import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

def init_db():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

def add_task():
    task = simpledialog.askstring("Add Task", "Enter your task:")
    if task:
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        conn.close()
        refresh_list()

def view_tasks():
    conn = sqlite3.connect('todo.db')
    c = conn.cursor()
    c.execute("SELECT id, task, status FROM tasks")
    tasks = c.fetchall()
    conn.close()
    return tasks

def mark_completed():
    selected_id = simpledialog.askstring("Mark Completed", "Enter task ID to mark as completed:")
    if selected_id and selected_id.isdigit():
        selected_id = int(selected_id)
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("UPDATE tasks SET status='completed' WHERE id=?", (selected_id,))
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Task marked as completed!")
        else:
            messagebox.showerror("Error", "Task ID not found.")
        conn.commit()
        conn.close()
        refresh_list()
    else:
        messagebox.showerror("Error", "Please enter a valid numeric task ID.")

def delete_task():
    selected_id = simpledialog.askstring("Delete Task", "Enter task ID to delete:")
    if selected_id and selected_id.isdigit():
        selected_id = int(selected_id)
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id=?", (selected_id,))
        if c.rowcount > 0:
            messagebox.showinfo("Success", "Task deleted!")
        else:
            messagebox.showerror("Error", "Task ID not found.")
        conn.commit()
        conn.close()
        refresh_list()
    else:
        messagebox.showerror("Error", "Please enter a valid numeric task ID.")

def refresh_list():
    listbox.delete(0, tk.END)
    tasks = view_tasks()
    for task in tasks:
        status = '✓' if task[2] == 'completed' else ' '
        listbox.insert(tk.END, f"ID: {task} - {status} {task[1]}")

root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x400")

listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(padx=20, pady=20)

btn_add = tk.Button(root, text="Add Task", command=add_task)
btn_add.pack(side=tk.LEFT, padx=20, pady=20)

btn_complete = tk.Button(root, text="Mark Completed", command=mark_completed)
btn_complete.pack(side=tk.LEFT, padx=5, pady=5)

btn_delete = tk.Button(root, text="Delete Task", command=delete_task)
btn_delete.pack(side=tk.LEFT, padx=5, pady=5)

init_db()
refresh_list()
root.mainloop()

