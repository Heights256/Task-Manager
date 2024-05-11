import tkinter as tk
import sqlite3
from tkinter import messagebox

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        # Initialize database connection
        self.conn = sqlite3.connect('tasks.db')
        self.create_table()

        # Create task button
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)

        # Task listbox
        self.task_listbox = tk.Listbox(self.root, width=50)
        self.task_listbox.pack()

        # Load tasks from database
        self.load_tasks()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                          (id INTEGER PRIMARY KEY, title TEXT, description TEXT, due_date TEXT, priority TEXT, category TEXT)''')
        self.conn.commit()

    def load_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        for task in tasks:
            self.tasks.append({
                "id": task[0],
                "Title": task[1],
                "Description": task[2],
                "Due Date": task[3],
                "Priority": task[4],
                "Category": task[5]
            })
            self.task_listbox.insert(tk.END, task[1])

    def add_task(self):
        # Add a new window to add task details
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Add Task")

        # Entry fields for task details
        tk.Label(add_task_window, text="Title:").pack()
        title_entry = tk.Entry(add_task_window)
        title_entry.pack()

        tk.Label(add_task_window, text="Due Date:").pack()
        due_date_entry = tk.Entry(add_task_window)
        due_date_entry.pack()

        tk.Label(add_task_window, text="Description:").pack()
        description_entry = tk.Entry(add_task_window)
        description_entry.pack()

        tk.Label(add_task_window, text="Priority:").pack()
        priority_entry = tk.Entry(add_task_window)
        priority_entry.pack()

        tk.Label(add_task_window, text="Category:").pack()
        category_entry = tk.Entry(add_task_window)
        category_entry.pack()

        # Save task button
        save_button = tk.Button(add_task_window, text="Save", command=lambda: self.save_task(
            title_entry.get(), description_entry.get(), due_date_entry.get(), priority_entry.get(), category_entry.get(), add_task_window))
        save_button.pack()

    def save_task(self, title, description, due_date, priority, category, window):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, due_date, priority, category) VALUES (?, ?, ?, ?, ?)",
                       (title, description, due_date, priority, category))
        self.conn.commit()

        # Update task listbox
        self.task_listbox.insert(tk.END, title)

        # Close add task window
        window.destroy()

# Main
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()