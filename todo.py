import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List App")
        self.root.geometry("400x350")

        # Widgets
        self.listbox = tk.Listbox(self.root, width=50, height=15)
        self.listbox.pack(padx=20, pady=10)

        self.btn_add = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.btn_add.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_complete = tk.Button(self.root, text="Mark Completed", command=self.mark_completed)
        self.btn_complete.pack(side=tk.LEFT, padx=10, pady=0)

        self.btn_delete = tk.Button(self.root, text="Delete Task", command=self.delete_task)
        self.btn_delete.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_refresh = tk.Button(self.root, text="Refresh", command=self.refresh_list)
        self.btn_refresh.pack(side=tk.LEFT, padx=10, pady=10)

        # Initialize database and refresh list
        self.init_db()
        self.refresh_list()

    def init_db(self):
        with sqlite3.connect('todo.db') as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task TEXT NOT NULL,
                    status TEXT DEFAULT 'pending'
                )
            ''')
            conn.commit()

    def view_tasks(self):
        with sqlite3.connect('todo.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, task, status FROM tasks")
            return c.fetchall()

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter your task:")
        if task:
            with sqlite3.connect('todo.db') as conn:
                c = conn.cursor()
                c.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
                conn.commit()
            self.refresh_list()

    def mark_completed(self):
        selected = simpledialog.askstring("Mark Completed", "Enter task ID:")
        if selected and selected.isdigit():
            selected_id = int(selected)
            with sqlite3.connect('todo.db') as conn:
                c = conn.cursor()
                c.execute("UPDATE tasks SET status='completed' WHERE id=?", (selected_id,))
                if c.rowcount > 0:
                    messagebox.showinfo("Success", "Task marked as completed!")
                else:
                    messagebox.showerror("Error", "Task ID not found.")
                conn.commit()
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Please enter a valid numeric task ID.")

    def delete_task(self):
        selected = simpledialog.askstring("Delete Task", "Enter task ID:")
        if selected and selected.isdigit():
            selected_id = int(selected)
            with sqlite3.connect('todo.db') as conn:
                c = conn.cursor()
                c.execute("DELETE FROM tasks WHERE id=?", (selected_id,))
                if c.rowcount > 0:
                    messagebox.showinfo("Success", "Task deleted!")
                else:
                    messagebox.showerror("Error", "Task ID not found.")
                conn.commit()
            self.refresh_list()
        else:
            messagebox.showerror("Error", "Please enter a valid numeric task ID.")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        tasks = self.view_tasks()
        for task in tasks:
            status = '✓' if task[2] == 'completed' else ' '
            self.listbox.insert(tk.END, f"{status} {task[1]} (ID: {task})")

# Main application entry point
if __name__ == '__main__':
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()

