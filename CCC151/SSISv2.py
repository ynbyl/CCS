import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk

# Create the Main Window
root = Tk()
root.title("Simple Student Information System V2.0")
root.geometry("600x450")
root.resizable(False, False)
my_tree = ttk.Treeview(root)

conn = sqlite3.connect("v2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    course TEXT,
                    year TEXT,
                    gender TEXT)''')

# To courses dropdown menu
cursor.execute("SELECT coursecode FROM courses")
courses = cursor.fetchall()
course_codes = [course[0] for course in courses]


# Function para wala hasol
def rtv():
    # clear
    my_tree.delete(*my_tree.get_children())

    # Fetch
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    # Insert
    for idx, row in enumerate(rows):
        my_tree.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[1], row[3], row[4], row[2]))


# Function to ADD student
def add_student():
    name = name_entry.get() or "-"
    year = year_entry.get() or "-"
    gender = gender_entry.get() or "-"
    course = course_entry.get() or "-"

    # Add to SQL
    cursor.execute(
        "INSERT INTO students (name, course, year, gender) VALUES (?, ?, ?, ?)",
        (name, course, year, gender))
    conn.commit()

    # Clear & Refresh
    name_entry.delete(0, tk.END)
    year_entry.set("")
    gender_entry.set("")
    course_entry.set("")

    rtv()


# Function to DELETE student
def delete_student():
    # Get the selected item from the tree view
    selected_item = my_tree.selection()
    if not selected_item:
        return

    # Get the ID of the selected student
    item_id = my_tree.item(selected_item)["text"]

    # Delete from SQL using ID
    cursor.execute("DELETE FROM students WHERE id=?", (item_id,))
    conn.commit()

    # Delete selected
    my_tree.delete(selected_item)

    rtv()


# Function to UPDATE student
def update_student():
    # Get the selected item from the tree view
    selected_item = my_tree.selection()
    if not selected_item:
        return

    # Get the ID of the selected student
    item_id = my_tree.item(selected_item)["text"]

    # Get the current values of the selected student
    current_values = my_tree.item(selected_item)["values"]

    # Get the updated values from the entry fields
    name = name_entry.get() or current_values[0]
    year = year_entry.get() or current_values[1]
    gender = gender_entry.get() or current_values[2]
    course = course_entry.get() or current_values[3]

    # Update the student's data in SQL
    cursor.execute(
        "UPDATE students SET name=?, course=?, year=?, gender=? WHERE id=?",
        (name, course, year, gender, item_id))
    conn.commit()

    # Clear & Refresh
    name_entry.delete(0, tk.END)
    year_entry.set("")
    gender_entry.set("")
    course_entry.set("")

    rtv()

# Buttons
add_button = tk.Button(root, text="Add Student", command=add_student)
add_button.grid(row=4, column=1, padx=5, pady=5)

del_button = tk.Button(root, text="Delete Student", command=delete_student)
del_button.grid(row=2, column=2, padx=5, pady=5)

upd_button = tk.Button(root, text="Edit", command=update_student)
upd_button.grid(row=1, column=2, padx=5, pady=5)

# Student Information Form
name_label = tk.Label(root, text="Full Name")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

course_label = tk.Label(root, text="Courses")
course_label.grid(row=3, column=0, padx=5, pady=5)
course_entry = ttk.Combobox(root, state="readonly", values=course_codes)
course_entry.grid(row=3, column=1, padx=5, pady=5)

year_label = tk.Label(root, text="Year Level:")
year_label.grid(row=1, column=0, padx=5, pady=5)
year_entry = ttk.Combobox(root, values=["Highschool", "1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"],
                          state="readonly")
year_entry.grid(row=1, column=1, padx=5, pady=5)

gender_label = tk.Label(root, text="Gender:")
gender_label.grid(row=2, column=0, padx=5, pady=5)
gender_entry = ttk.Combobox(root, values=["Male", "Female"], state="readonly")
gender_entry.grid(row=2, column=1, padx=5, pady=5)

search_label = tk.Label(root, text="Search Student Below")
search_label.grid(row=5, column=0, padx=5, pady=5)
search_entry = tk.Entry(root)
search_entry.grid(row=5, column=1, padx=5, pady=5)

# Treeview
my_tree = ttk.Treeview(root)
my_tree["columns"] = ("name", "year", "gender", "course")
my_tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

my_tree.heading("#0", text="ID")
my_tree.heading("name", text="Fullname")
my_tree.heading("year", text="Year Level")
my_tree.heading("gender", text="Gender")
my_tree.heading("course", text="Course")

my_tree.column("#0", width=0, stretch=tk.NO)
my_tree.column("name", width=250, anchor=tk.CENTER)
my_tree.column("year", width=100, anchor=tk.CENTER)
my_tree.column("gender", width=100, anchor=tk.CENTER)
my_tree.column("course", width=140, anchor=tk.CENTER)

rtv()
root.mainloop()
