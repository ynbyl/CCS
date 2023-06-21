import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk
import subprocess




# Create the Main Window
root = Tk()
root.title("Simple Student Information System V2.0")
root.geometry("600x450")
root.resizable(False, False)
student_list = ttk.Treeview(root)

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
    student_list.delete(*student_list.get_children())

    # Fetch
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    # Insert
    for idx, row in enumerate(rows):
        student_list.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[1], row[3], row[4], row[2]))


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
    selected_item = student_list.selection()
    if not selected_item:
        return

    # Get the ID of the selected student
    item_id = student_list.item(selected_item)["text"]

    # Delete from SQL using ID
    cursor.execute("DELETE FROM students WHERE id=?", (item_id,))
    conn.commit()

    # Delete selected
    student_list.delete(selected_item)

    rtv()


# Function to UPDATE student
def update_student():
    # Get the selected item from the tree view
    selected_item = student_list.selection()
    if not selected_item:
        return

    # Get the ID of the selected student
    item_id = student_list.item(selected_item)["text"]

    # Get the current values of the selected student
    current_values = student_list.item(selected_item)["values"]

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


# Function to search for students by any column
def search():
    search_text = search_entry.get()

    # Clear previous search if gikan search
    student_list.tag_configure("highlight", background="yellow")

    # Iterate over the items in the Treeview
    for item in student_list.get_children():
        values = student_list.item(item)["values"]
        found = False

        # Check if the search text matches any value in the current item
        for value in values:
            if search_text.lower() in value.lower():
                found = True
                break

        # Highlights
        if found:
            student_list.item(item, tags=("highlight",))
        else:
            student_list.item(item, tags=())

    # Reset the search entry
    search_entry.delete(0, tk.END)


# Function to OPEN course.py
def open_program():
    program_path = "C:/Users/roelb/PycharmProjects/pythonProject2/coursesV2.py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")

    root.destroy()




# Buttons
add_button = tk.Button(root, text="Add Student", command=add_student)
add_button.grid(row=4, column=1, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Student", command=delete_student)
delete_button.grid(row=3, column=2, padx=5, pady=5)

update_button = tk.Button(root, text="Edit", command=update_student)
update_button.grid(row=2, column=2, padx=5, pady=5)

search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=5, column=2, padx=5, pady=5)

course_button = tk.Button(root, text="Courses", command=open_program)
course_button.grid(row=0, column=2, padx=5, pady=5)




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

search_label = tk.Label(root, text="Search Student")
search_label.grid(row=5, column=0, padx=5, pady=5)
search_entry = tk.Entry(root)
search_entry.grid(row=5, column=1, padx=5, pady=5)




# Treeview
student_list = ttk.Treeview(root)
student_list["columns"] = ("name", "year", "gender", "course")
student_list.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

student_list.heading("#0", text="ID")
student_list.heading("name", text="Fullname")
student_list.heading("year", text="Year Level")
student_list.heading("gender", text="Gender")
student_list.heading("course", text="Course")

student_list.column("#0", width=0, stretch=tk.NO)
student_list.column("name", width=250, anchor=tk.CENTER)
student_list.column("year", width=100, anchor=tk.CENTER)
student_list.column("gender", width=100, anchor=tk.CENTER)
student_list.column("course", width=140, anchor=tk.CENTER)

rtv()
root.mainloop()
