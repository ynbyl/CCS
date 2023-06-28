import sqlite3
import subprocess
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

# Create the Main Window
root = Tk()
root.title("Simple Student Information System V2.0")
root.geometry("600x480")
root.resizable(False, False)
student_list = ttk.Treeview(root)

conn = sqlite3.connect("ssis.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                    studid TEXT PRIMARY KEY,
                    name TEXT,
                    coursecode TEXT,
                    year TEXT,
                    gender TEXT,
                    FOREIGN KEY (coursecode) REFERENCES courses(coursecode))''')
    w
cursor.execute("SELECT coursecode FROM courses")
courses = cursor.fetchall()
course_codes = [course[0] for course in courses]


# Functions
def rtv():
    student_list.delete(*student_list.get_children())

    # Fetch
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    # Insert data sa tv
    for idx, row in enumerate(rows):
        student_list.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[0], row[1], row[3], row[4], row[2]))


def add_student():
    # Retrieve
    studid = id_entry.get().strip()
    name = name_entry.get().strip()
    year = year_entry.get().strip()
    course = course_entry.get().strip()
    gender = gender_entry.get().strip()

    # Fil up validation
    if not studid or not name or not year or not course or not gender:
        messagebox.showerror("Error", "Please fill in all the fields.")
        return

    # Duplication
    cursor.execute("SELECT COUNT(*) FROM students WHERE studid = ?", (studid,))
    if cursor.fetchone()[0] > 0:
        messagebox.showerror("Error", "Student ID already exists.")
        return

    # Add data to the treeview
    student_list.insert("", "end", text=studid, values=(studid, name, year, gender, course))

    # Insert data into the database
    cursor.execute("INSERT INTO students (studid, name, coursecode, year, gender) VALUES (?, ?, ?, ?, ?)",
                   (studid, name, course, year, gender))
    conn.commit()

    id_entry.delete(0, END)
    name_entry.delete(0, END)
    year_entry.set("")
    course_entry.set("")
    gender_entry.set("")

    rtv()

def delete_student():
    selected_item = student_list.selection()

    if not selected_item:
        messagebox.showerror("Error", "No student selected.")
        return

    # Validation
    confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the selected student?")
    if not confirm:
        return

    # Retrieve the student ID from the selected item
    studid = student_list.item(selected_item, "text")

    # Remove the selected student from the treeview
    student_list.delete(selected_item)

    # Delete the student from the database
    cursor.execute("DELETE FROM students WHERE studid = ?", (studid,))
    conn.commit()


    rtv()

def update_student():
    selected_item = student_list.selection()
    if not selected_item:
        return

    # Disable the student ID entry field
    id_entry.configure(state="disabled")

    # Get the current values of the selected student
    current_values = student_list.item(selected_item)["values"]

    # Enable the name, year, course, and gender entry fields for editing
    name_entry.configure(state="normal")
    year_entry.configure(state="readonly")
    course_entry.configure(state="readonly")
    gender_entry.configure(state="readonly")

    # Populate the entry fields with the current values
    name_entry.delete(0, tk.END)
    name_entry.insert(0, current_values[1])
    year_entry.set(current_values[2])
    course_entry.set(current_values[4])
    gender_entry.set(current_values[3])

    # Define the confirm_update function
    def confirm_update(studid):
        # Get the updated values from the entry fields
        name = name_entry.get()
        year = year_entry.get()
        course = course_entry.get()
        gender = gender_entry.get()

        # Ask for confirmation using a dialogue prompt
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to update this student?")

        if confirm:
            # Update the student data in the database
            cursor.execute(
                "UPDATE students SET name=?, year=?, coursecode=?, gender=? WHERE studid=?",
                (name, year, course, gender, studid))
            conn.commit()

            # Clear entry fields and refresh the tree view
            id_entry.configure(state="normal")
            name_entry.delete(0, tk.END)
            year_entry.set("")
            course_entry.set("")
            gender_entry.set("")

            # Change the text and command of the update_button back to its original state
            update_button.configure(text="Edit", command=update_student)

            rtv()

    # Get the student ID of the selected student
    studid = current_values[0]

    # Change the text and command of the update_button
    update_button.configure(text="Confirm", command=lambda: confirm_update(studid))


def search():
    query = search_entry.get().strip()

    student_list.delete(*student_list.get_children())
    cursor.execute("SELECT * FROM students WHERE studid LIKE ? OR name LIKE ? OR coursecode LIKE ? OR year LIKE ? OR gender LIKE ?",
                   (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
    rows = cursor.fetchall()

    # Insert to tv
    for idx, row in enumerate(rows):
        student_list.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[0], row[1], row[3], row[4], row[2]))


    search_entry.delete(0, END)


def open_program():
    program_path = "D:/Downloads/SSIS/sis(3).py"
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
year_entry = ttk.Combobox(root, values=["Highschool", "1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"], state="readonly")
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
student_list["columns"] = ("studid", "name", "year", "gender", "course")
student_list.grid(row=7, column=0, columnspan=3, padx=5, pady=5)

student_list.heading("#0", text="ID")
student_list.heading("studid", text="Student ID")
student_list.heading("name", text="Full Name")
student_list.heading("year", text="Year Level")
student_list.heading("gender", text="Gender")
student_list.heading("course", text="Course")

student_list.column("#0", width=0, stretch=tk.NO)
student_list.column("studid", width=80, anchor=tk.CENTER)
student_list.column("name", width=230, anchor=tk.CENTER)
student_list.column("year", width=100, anchor=tk.CENTER)
student_list.column("gender", width=80, anchor=tk.CENTER)
student_list.column("course", width=100, anchor=tk.CENTER)

rtv()
root.mainloop()
