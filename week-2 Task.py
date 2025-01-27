import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import logging
logging.basicConfig(filename="calculator.log", level=logging.INFO, format="%(asctime)s - %(message)s")
def init_db():
    conn = sqlite3.connect("calculator_history.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS history (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  operation TEXT,
                  result TEXT,
                  timestamp TEXT)''')
    conn.commit()
    conn.close()
init_db()
def save_to_db(operation, result):
    conn = sqlite3.connect("calculator_history.db")
    c = conn.cursor()
    c.execute("INSERT INTO history (operation, result, timestamp) VALUES (?, ?, ?)", (operation, result, datetime.now()))
    conn.commit()
    conn.close()
def get_history():
    conn = sqlite3.connect("calculator_history.db")
    c = conn.cursor()
    c.execute("SELECT * FROM history")
    rows = c.fetchall()
    conn.close()
    return rows
def calculate(operation):
    try:
        result = eval(operation)
        save_to_db(operation, str(result))
        logging.info(f"Operation: {operation}, Result: {result}")
        return result
    except ZeroDivisionError:
        logging.error("Attempted division by zero.")
        return "Error: Division by zero"
    except Exception as e:
        logging.error(f"Invalid input: {operation}. Error: {e}")
        return "Error: Invalid input"
def create_gui():
    def append_to_expression(value):
        current = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, current + value)
    def clear_expression():
        entry.delete(0, tk.END)
    def evaluate_expression():
        expression = entry.get()
        result = calculate(expression)
        entry.delete(0, tk.END)
        entry.insert(0, result)
    def show_history():
        history = get_history()
        history_text = "\n".join([f"{row[1]} = {row[2]} (at {row[3]})" for row in history])
        messagebox.showinfo("History", history_text if history_text else "No history available.")
    root = tk.Tk()
    root.title("Calculator with Digital Clock")
    def update_clock():
        now = datetime.now().strftime("%H:%M:%S")
        clock_label.config(text=now)
        root.after(1000, update_clock)
    clock_label = tk.Label(root, text="", font=("Helvetica", 16))
    clock_label.pack()
    update_clock()
    entry = tk.Entry(root, font=("Helvetica", 14), justify="right")
    entry.pack(fill=tk.BOTH, padx=10, pady=10)
    button_frame = tk.Frame(root)
    button_frame.pack()
    buttons = [
        ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
        ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
        ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
        ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ]
    for (text, row, col) in buttons:
        if text == "=":
            tk.Button(button_frame, text=text, width=5, height=2, command=evaluate_expression).grid(row=row, column=col, padx=5, pady=5)
        else:
            tk.Button(button_frame, text=text, width=5, height=2, command=lambda t=text: append_to_expression(t)).grid(row=row, column=col, padx=5, pady=5)
    tk.Button(root, text="C", width=5, height=2, command=clear_expression).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(root, text="History", width=10, height=2, command=show_history).pack(side=tk.RIGHT, padx=5, pady=5)
    root.mainloop()
if __name__ == "__main__":
    create_gui()
