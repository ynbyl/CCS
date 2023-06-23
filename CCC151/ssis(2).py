import sqlite3
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Create the Main Window
root = Tk()
root.title("Simple Student Information System V2.0")
root.geometry("600x480")
root.resizable(False, False)
student_list = ttk.Treeview(root)

conn = sqlite3.connect("version2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    studid TEXT,
                    name TEXT,
                    course TEXT,
                    year TEXT,
                    gender TEXT)''')

cursor.execute("SELECT coursecode FROM courses")
courses = cursor.fetchall()
course_codes = [course[0] for course in courses]


# Function to clear and refresh the student list
def rsl():
    # Clear the student list
    student_list.delete(*student_list.get_children())

    # Fetch data from the database
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    # Insert data into the student list
    for idx, row in enumerate(rows):
        student_list.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[1], row[2], row[4], row[5], row[3]))


# Function to ADD a student
def add_student():
    studid = id_entry.get() or "-"
    name = name_entry.get() or "-"
    year = year_entry.get() or "-"
    gender = gender_entry.get() or "-"
    course = course_entry.get() or "-"

    # DB
    cursor.execute("INSERT INTO students (studid, name, course, year, gender) VALUES (?, ?, ?, ?, ?)",
                   (studid, name, course, year, gender))
    conn.commit()

    # Clear and refresh
    name_entry.delete(0, tk.END)
    id_entry.delete(0, tk.END)
    year_entry.set("")
    gender_entry.set("")
    course_entry.set("")

    rsl()


# Function to DELETE selected students
def delete_student():
    # Get the selected items from the tree view
    selected_items = student_list.selection()
    if not selected_items:
        return

    confirm = messagebox.askyesno("Hold up!", "Are you absolutely sure you want to confirm deletion?")

    if confirm:
        # Iterate over selected items
        for item_id in selected_items:
            # Get the ID of the selected student
            student_id = student_list.item(item_id)["text"]

            try:
                # Delete the student from the database using ID
                cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
                conn.commit()

                # Delete the selected student from the tree view
                student_list.delete(item_id)
            except tk.TclError:
                pass

        rsl()




# Function to UPDATE a student
def update_student():
    # Get the selected item from the tree view
    selected_item = student_list.selection()
    if not selected_item:
        return

    # Retrieve the selected student's information
    item_id = student_list.item(selected_item)["text"]
    studid = student_list.item(selected_item)["values"][0]
    name = student_list.item(selected_item)["values"][1]
    year = student_list.item(selected_item)["values"][2]
    gender = student_list.item(selected_item)["values"][3]
    course = student_list.item(selected_item)["values"][4]

    # Copy the selected student's information into the entry fields and dropdown
    id_entry.delete(0, tk.END)
    id_entry.insert(0, studid)
    name_entry.delete(0, tk.END)
    name_entry.insert(0, name)
    year_entry.set(year)
    gender_entry.set(gender)
    course_entry.set(course)

    # Function to save the changes and update the student's information
    def save_changes():
        # Ask for confirmation using a messagebox
        confirm = messagebox.askyesno("Confirm Changes", "Are you absolutely sure you want to proceed?")

        if confirm:
            # Get the modified values from the entry fields and dropdown
            modified_studid = id_entry.get() or "-"
            modified_name = name_entry.get() or "-"
            modified_year = year_entry.get() or "-"
            modified_gender = gender_entry.get() or "-"
            modified_course = course_entry.get() or "-"

            # Update the student's information in the database with the modified values
            cursor.execute("UPDATE students SET studid=?, name=?, course=?, year=?, gender=? WHERE id=?",
                           (modified_studid, modified_name, modified_course, modified_year, modified_gender, item_id))
            conn.commit()

            # Clear the input fields and refresh the student list
            id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            year_entry.set("")
            gender_entry.set("")
            course_entry.set("")
            rsl()

            # Destroy the save button after clicking it
            save_button.destroy()

    # Create a save button to save the changes
    save_button = tk.Button(root, text="Save Changes", command=save_changes, bg="#abdbe3")
    save_button.grid(row=3, column=2, padx=5, pady=5)


# Function to SEARCH for students by any column
def search():
    search_text = search_entry.get()
    student_list.selection_remove(student_list.selection())

    # Clear the student list
    student_list.delete(*student_list.get_children())

    # Fetch data from the database
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    # Insert matching data into the student list
    for idx, row in enumerate(rows):
        values = (row[1], row[2], row[4], row[5], row[3])
        found = False

        # Check if the search text matches any value in the current row
        for value in values:
            if search_text.lower() in str(value).lower():
                found = True
                break

        # Insert the matching row into the student list
        if found:
            student_list.insert(parent="", index=idx, iid=idx, text=row[0], values=values)

    # Reset the search entry
    search_entry.delete(0, tk.END)

# Function to OPEN courses
def open_program():
    program_path = "D:/Downloads/SSIS/courses(2).py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")

    root.destroy()

# Buttons
add_button = tk.Button(root, text="Add Student", command=add_student, bg="#abdbe3")
add_button.grid(row=5, column=1, padx=5, pady=5)

delete_button = tk.Button(root, text="Delete Student", command=delete_student, bg="#F77070")
delete_button.grid(row=4, column=2, padx=5, pady=5)

update_button = tk.Button(root, text="Edit", command=update_student)
update_button.grid(row=2, column=2, padx=5, pady=5)

search_button = tk.Button(root, text="Search", command=search)
search_button.grid(row=6, column=2, padx=5, pady=5)

course_button = tk.Button(root, text="Courses", command=open_program, bg="#eab676")
course_button.grid(row=0, column=2, padx=5, pady=5)

# Student Information Form
name_label = tk.Label(root, text="Full Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=5, pady=5)

id_label = tk.Label(root, text="Student ID:")
id_label.grid(row=1, column=0, padx=5, pady=5)
id_entry = tk.Entry(root)
id_entry.grid(row=1, column=1, padx=5, pady=5)

year_label = tk.Label(root, text="Year Level:")
year_label.grid(row=2, column=0, padx=5, pady=5)
year_entry = ttk.Combobox(root, values=["Highschool", "1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"],
                          state="readonly")
year_entry.grid(row=2, column=1, padx=5, pady=5)

course_label = tk.Label(root, text="Courses:")
course_label.grid(row=3, column=0, padx=5, pady=5)
course_entry = ttk.Combobox(root, state="readonly", values=course_codes)
course_entry.grid(row=3, column=1, padx=5, pady=5)

gender_label = tk.Label(root, text="Gender:")
gender_label.grid(row=4, column=0, padx=5, pady=5)
gender_entry = ttk.Combobox(root, values=["Male", "Female"], state="readonly")
gender_entry.grid(row=4, column=1, padx=5, pady=5)

search_label = tk.Label(root, text="Search Student:")
search_label.grid(row=6, column=0, padx=5, pady=5)
search_entry = tk.Entry(root)
search_entry.grid(row=6, column=1, padx=5, pady=5)

# Treeview
student_list = ttk.Treeview(root)
student_list["columns"] = ("id", "name", "year", "gender", "course")
student_list.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

student_list.heading("#0", text="ID")
student_list.heading("id", text="Student ID")
student_list.heading("name", text="Full Name")
student_list.heading("year", text="Year Level")
student_list.heading("gender", text="Gender")
student_list.heading("course", text="Course")

student_list.column("#0", width=0, stretch=tk.NO)
student_list.column("id", width=80, anchor=tk.CENTER)
student_list.column("name", width=230, anchor=tk.CENTER)
student_list.column("year", width=100, anchor=tk.CENTER)
student_list.column("gender", width=80, anchor=tk.CENTER)
student_list.column("course", width=100, anchor=tk.CENTER)

rsl()
root.mainloop()
