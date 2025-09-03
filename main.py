import tkinter as tk
from tkinter import messagebox
import sqlite3


conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        status TEXT NOT NULL
    )
""")
conn.commit()

def load_tasks():
    task_list.delete(0, tk.END)
    cursor.execute("SELECT id, task, status FROM tasks")
    for row in cursor.fetchall():
        display_text = f"[{'✔' if row[2] == 'done' else ' '}] {row[1]}"
        task_list.insert(tk.END, display_text)

def add_task():
    task = entry_task.get()
    if task.strip() == "":
        messagebox.showwarning("Warning", "Task cannot be empty!")
        return
    cursor.execute("INSERT INTO tasks (task, status) VALUES (?, ?)", (task, "pending"))
    conn.commit()
    entry_task.delete(0, tk.END)
    load_tasks()

def delete_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No task selected!")
        return
    index = selected[0]
    cursor.execute("SELECT id FROM tasks")
    task_id = cursor.fetchall()[index][0]
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    load_tasks()

def mark_complete():
    selected = task_list.curselection()
    if not selected:
        messagebox.showwarning("Warning", "No task selected!")
        return
    index = selected[0]
    cursor.execute("SELECT id FROM tasks")
    task_id = cursor.fetchall()[index][0]
    cursor.execute("UPDATE tasks SET status='done' WHERE id=?", (task_id,))
    conn.commit()
    load_tasks()
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")
root.config(bg="#f0f0f0")

title_label = tk.Label(root, text="To-Do List", font=("Arial", 18, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

entry_task = tk.Entry(frame, width=25, font=("Arial", 12))
entry_task.pack(side=tk.LEFT, padx=5)

add_button = tk.Button(frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white")
add_button.pack(side=tk.LEFT)

task_list = tk.Listbox(root, width=40, height=15, font=("Arial", 12))
task_list.pack(pady=10)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

complete_button = tk.Button(btn_frame, text="Mark Complete", command=mark_complete, bg="#2196F3", fg="white")
complete_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(btn_frame, text="Delete Task", command=delete_task, bg="#f44336", fg="white")
delete_button.grid(row=0, column=1, padx=5)

load_tasks()

root.mainloop()
