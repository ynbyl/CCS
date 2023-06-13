import tkinter as tk
import customtkinter
import subprocess


# Create the main window
root = customtkinter.CTk()
root.title("Courses Information System")
root.configure(bg="#2a2d30")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


# A class to represent a student and store their information
class Student:
    def __init__(self, course, course_code):
        self.course = course
        self.course_code = course_code


# Function to retrieve data saved when executable was exited
def load_courses():
    global list_data
    list_data = []
    try:
        with open("courses.txt", "r", encoding="utf-8") as file:
            for f in file:
                listbox.insert(tk.END, f.strip())
                list_data.append(f.strip())
    except:
        pass

# Function to add course to the list
def add(event=None):
    global list_data
    course = course_entry.get()
    course_code = course_code_entry.get()  # Retrieve the course code

    student = Student(course, course_code)  # Pass the course code as an argument
    student_info = f"{student.course} | {student.course_code}"  # Include course code in the string
    listbox.insert(tk.END, student_info)
    list_data.append(student_info)

    # Clear the entry fields
    course_entry.delete(0, 'end')
    course_code_entry.delete(0, 'end')


# Function to "Edit" or simply replace course
def edit_selected():
    selected_index = listbox.curselection()
    if selected_index:
        selected_text = listbox.get(selected_index[0])
        # Extract the course and course code from the selected text
        course, _, course_code = selected_text.partition(" | ")
        course_entry.delete(0, tk.END)
        course_entry.insert(0, course)
        course_code_entry.delete(0, tk.END)
        course_code_entry.insert(0, course_code)
        delete_selected()


# Function to delete ALL of the course lists
def delete():
    global list_data
    listbox.delete(0, tk.END)
    list_data = []


# Function to delete the selected course from the list
def delete_selected():
    global list_data

    try:
        index = listbox.curselection()[0]
        selected = list_data[index]
        listbox.delete(tk.ANCHOR)
        list_data.pop(index)
    except:
        pass

# Function to save the course data to a file and exit the program
def quit():
    global root
    with open("courses.txt", "w", encoding="utf-8") as file:
        for d in list_data:
            file.write(d + "\n")
    root.destroy()

    program_path = "C:/Users/roelb/PycharmProjects/pythonProject2/SIS.py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")



# Student Information Form
course_label = customtkinter.CTkLabel(root, text="Course:")
course_label.grid(row=0, column=0, padx=10, pady=10)
course_code_label = customtkinter.CTkLabel(root, text="Course Code:")
course_code_label.grid(row=1, column=0, padx=10, pady=10)

course_entry = customtkinter.CTkEntry(root)
course_entry.grid(row=0, column=1, padx=10, pady=10)
course_code_entry = customtkinter.CTkEntry(root)
course_code_entry.grid(row=1, column=1, padx=10, pady=10)

# Create a button to add a new student
root.bind('<Return>', add)

# Create a button to edit selected
button_edit = customtkinter.CTkButton(root, text="Edit Course", command=edit_selected)
button_edit.grid(row=2, column=2, padx=10, pady=10)

# Create a button to deletes ALL inputs
button_delete = customtkinter.CTkButton(root, text="Remove All Courses", command=delete)
button_delete.grid(row=2, column=0, padx=10, pady=10)

# Create a button to delete SELECTED input
button_delete_selected = customtkinter.CTkButton(root, text="Remove Selected Course", command=delete_selected)
button_delete_selected.grid(row=2, column=1, padx=10, pady=10)

# Create the listbox
listbox = tk.Listbox(root)
listbox.grid(row=7, columnspan=5, padx=10, pady=20)
listbox.configure(bg="#252524", fg="white")

# Create a button to Save and Quit
bquit = customtkinter.CTkButton(root, text="Return to Student List", command=quit)
bquit.grid(row=9, column=1, padx=10, pady=10)

load_courses()
root.mainloop()
