import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk




# Create the Main Window
root = Tk()
root.title("Courses Information Management V2.0")
root.geometry("600x400")
root.resizable(False, False)
my_tree = ttk.Treeview(root)

conn = sqlite3.connect("v2.db")
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    coursecode TEXT,
                    coursename TEXT)''')




# Function to fetch and display courses
def rtv():
    # Clear the tree view
    my_tree.delete(*my_tree.get_children())

    # Fetch courses from the database
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()

    # Insert courses into the tree view
    for idx, row in enumerate(rows):
        my_tree.insert(parent="", index=idx, iid=idx, text=row[0], values=(row[1], row[2]))


# Function to add a course
def add_course():
    coursecode = coursecode_entry.get() or "-"
    coursename = coursename_entry.get() or "-"

    # Add course to the database
    cursor.execute(
        "INSERT INTO courses (coursecode, coursename) VALUES (?, ?)",
        (coursecode, coursename))
    conn.commit()

    # Clear entry fields and refresh the tree view
    coursecode_entry.delete(0, tk.END)
    coursename_entry.delete(0, tk.END)

    rtv()


# Function to delete a course
def delete_course():
    # Get the selected item from the tree view
    selected_item = my_tree.selection()
    if not selected_item:
        return

    # Get the ID of the selected course
    item_id = my_tree.item(selected_item)["text"]

    # Delete the course from the database using ID
    cursor.execute("DELETE FROM courses WHERE id=?", (item_id,))
    conn.commit()

    # Delete the selected course from the tree view
    my_tree.delete(selected_item)

    rtv()


# Function to update a course
def update_course():
    # Get the selected item from the tree view
    selected_item = my_tree.selection()
    if not selected_item:
        return

    # Get the ID of the selected course
    item_id = my_tree.item(selected_item)["text"]

    # Get the current values of the selected course
    current_values = my_tree.item(selected_item)["values"]

    # Get the updated values from the entry fields
    coursecode = coursecode_entry.get() or current_values[0]
    coursename = coursename_entry.get() or current_values[1]

    # Update the course data in the database
    cursor.execute(
        "UPDATE courses SET coursecode=?, coursename=? WHERE id=?",
        (coursecode, coursename, item_id))
    conn.commit()

    # Clear entry fields and refresh the tree view
    coursecode_entry.delete(0, tk.END)
    coursename_entry.delete(0, tk.END)

    rtv()




# Buttons
add_button = tk.Button(root, text="Add Course", command=add_course)
add_button.grid(row=2, column=1, padx=5, pady=5)

del_button = tk.Button(root, text="Delete Course", command=delete_course)
del_button.grid(row=4, column=0, padx=5, pady=5)

upd_button = tk.Button(root, text="Update", command=update_course)
upd_button.grid(row=4, column=1, padx=5, pady=5)




# Course Information Form
coursecode_label = tk.Label(root, text="Course Code:")
coursecode_label.grid(row=0, column=0, padx=5, pady=5)
coursecode_entry = tk.Entry(root)
coursecode_entry.grid(row=0, column=1, padx=5, pady=5)

coursename_label = tk.Label(root, text="Course Name:")
coursename_label.grid(row=1, column=0, padx=5, pady=5)
coursename_entry = tk.Entry(root)
coursename_entry.grid(row=1, column=1, padx=5, pady=5)




# Treeview
my_tree = ttk.Treeview(root)
my_tree["columns"] = ("coursecode", "coursename")
my_tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

my_tree.heading("#0", text="ID")
my_tree.heading("coursecode", text="Course Code")
my_tree.heading("coursename", text="Course")

my_tree.column("#0", width=0, stretch=tk.NO)
my_tree.column("coursecode", width=150, anchor=tk.CENTER)
my_tree.column("coursename", width=440, anchor=tk.CENTER)




rtv()
root.mainloop()
