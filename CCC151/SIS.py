import tkinter as tk
import tkinter.ttk as ttk
import customtkinter
import subprocess
from tkinter import font




# Create the main window
root = customtkinter.CTk()
root.title("Student Information System")
root.configure(bg="#2a2d30")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")




# class to store and represent data
class Student:
    def __init__(self, name, id_num, course, year_level, gpa):
        self.name = name
        self.course = course
        self.id_num = id_num
        self.year_level = year_level
        self.gpa = gpa


# Function to retrieve data saved when exec is exited
def retrieve_data():
    global list_data

    list_data = []

    try:
        with open("save.txt", "r", encoding="utf-8") as file:
            for std in file:
                data = std.strip().split("     ")
                student_list.insert("", tk.END, values=(data[0], data[1], data[2], data[3], data[4]))
                list_data.append(std.strip())

    except:
        pass


# Function to retrieve data from "courses.txt" and populate the dropdown menu
def courses(course_entry):
    try:
        with open("courses.txt", "r", encoding="utf-8") as file:
            courses = [course.strip() for course in file]
            course_entry['values'] = courses
    except FileNotFoundError:
        print("courses.txt file not found.")


# Function to add student to the list
def add():
    global list_data

    first_name = first_name_entry.get()
    middle_initial = middle_initial_entry.get()
    last_name = last_name_entry.get()
    course = course_entry.get()
    id_num = id_entry.get()
    year_level = year_entry.get()
    gpa = gpa_entry.get()

    if first_name == "":
        first_name = "-"
    if middle_initial == "":
        middle_initial = "-"
    if last_name == "":
        last_name = "-"
    if course == "":
        course = "-"
    if id_num == "":
        id_num = "-"
    if year_level == "":
        year_level = "-"
    if gpa == "":
        gpa = "-"

    name = f"{first_name} {middle_initial} {last_name}"

    student = Student(name, id_num, course, year_level, gpa)
    student_info = (student.name, student.id_num, student.course, student.year_level, student.gpa)

    student_list.insert("", tk.END, values=student_info)
    list_data.append("     ".join(student_info))

    first_name_entry.delete(0, 'end')
    middle_initial_entry.delete(0, 'end')
    last_name_entry.delete(0, 'end')
    id_entry.delete(0, 'end')
    course_entry.delete(0, 'end')
    gpa_entry.delete(0, 'end')


# Function to "Edit" or simply replace students :)
def edit_selected():
    selected_item = student_list.selection()

    if selected_item:
        # Get the selected student's data
        values = student_list.item(selected_item)['values']
        name_entry.insert(0, values[0])
        id_entry.insert(0, values[1])
        course_entry.insert(0, values[2])
        year_entry.insert(0, values[3])
        gpa_entry.insert(0, values[4])
        delete_selected()


# Function to delete ALL students on the list
def delete():
    global list_data
    student_list.delete(*student_list.get_children())
    list_data = []


# Function to delete selected student from the list
def delete_selected():
    global list_data

    selected_item = student_list.selection()

    if selected_item:
        selected_index = int(selected_item[0][1:]) - 1
        student_list.delete(selected_item)

        del list_data[selected_index]


# Function to open courses program using subprocess
def open_program():
    program_path = "C:/Users/roelb/PycharmProjects/pythonProject2/courses.py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")
    root.destroy()


# Function to save the data to a text file and exit
def quit():
    global root
    with open("save.txt", "w", encoding="utf-8") as file:
        for d in list_data:
            file.write(d + "\n")
    root.destroy()


# Function to search for students by any column
def search():
    search_query = search_entry.get().strip().lower()
    if search_query:
        items = student_list.get_children("")
        student_list.selection_remove(*student_list.get_children())
        for item in items:
            values = student_list.item(item)["values"]
            if any(search_query in str(value).lower() for value in values):
                student_list.selection_add(item)
                student_list.focus(item)
                student_list.see(item)

                
                

# Student Information Form
first_name_label = customtkinter.CTkLabel(root, text="First Name:")
first_name_label.grid(row=0, column=0, padx=20, pady=20)
first_name_entry = customtkinter.CTkEntry(root)
first_name_entry.grid(row=0, column=1, padx=20, pady=20)

middle_initial_label = customtkinter.CTkLabel(root, text="Middle Initial:")
middle_initial_label.grid(row=1, column=0, padx=20, pady=20)
middle_initial_entry = customtkinter.CTkEntry(root)
middle_initial_entry.grid(row=1, column=1, padx=20, pady=20)

last_name_label = customtkinter.CTkLabel(root, text="Last Name:")
last_name_label.grid(row=2, column=0, padx=20, pady=20)
last_name_entry = customtkinter.CTkEntry(root)
last_name_entry.grid(row=2, column=1, padx=20, pady=20)

course_label = customtkinter.CTkLabel(root, text="Courses")
course_label.grid(row=3, column=0, padx=20, pady=20)
course_entry = ttk.Combobox(root, state="readonly")
course_entry.grid(row=3, column=1, padx=20, pady=20)
courses(course_entry)

id_label = customtkinter.CTkLabel(root, text="ID:")
id_label.grid(row=0, column=2, padx=20, pady=20)
id_entry = customtkinter.CTkEntry(root)
id_entry.grid(row=0, column=3, padx=20, pady=20)

year_label = customtkinter.CTkLabel(root, text="Year Level:")
year_label.grid(row=1, column=2, padx=20, pady=20)
year_entry = customtkinter.CTkComboBox(root, values=["Highschool", "1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"])
year_entry.grid(row=1, column=3, padx=20, pady=20)

gpa_label = customtkinter.CTkLabel(root, text="GPA:")
gpa_label.grid(row=2, column=2, padx=20, pady=20)
gpa_entry = customtkinter.CTkEntry(root)
gpa_entry.grid(row=2, column=3, padx=20, pady=20)

search_label = customtkinter.CTkLabel(root, text="Search Student")
search_label.grid(row=3, column=2, padx=20, pady=20)
search_entry = customtkinter.CTkEntry(root)
search_entry.grid(row=3, column=3, padx=20, pady=20)

# Button Search
search_button = customtkinter.CTkButton(root, text="Search", command=search)
search_button.grid(row=3, column=4, padx=20, pady=20)

# Button Add
large_font = customtkinter.CTkFont(size=30)

button = customtkinter.CTkButton(root, text="Add \n \n Student", command=add, height=100, font=large_font)
button.grid(row=0, column=4, padx=20, pady=20, rowspan=3)

# Button Edit
button_edit = customtkinter.CTkButton(root, text="Edit Selected Student", command=edit_selected)
button_edit.grid(row=4, column=3, padx=20, pady=20)

# Button Remove
button_delete_selected = customtkinter.CTkButton(root, text="Remove Selected Student", command=delete_selected)
button_delete_selected.grid(row=4, column=1, padx=20, pady=20)

# Button Clear
button_delete = customtkinter.CTkButton(root, text="Remove All Students", command=delete)
button_delete.grid(row=9, column=0, padx=20, pady=20)

# Button Course Window
button_open = customtkinter.CTkButton(root, text="Open Course Selection", command=open_program)
button_open.grid(row=9, column=2, padx=20, pady=20)

# Button SnQ
bquit = customtkinter.CTkButton(root, text="Save and Quit", command=quit)
bquit.grid(row=9, column=4, padx=20, pady=20)




# # Create a TreeView to display the student information
style = ttk.Style()
style.theme_use("default")
style.configure("mystyle.Treeview.Heading", font=('Calibri', 12, 'bold'), background="#1f6ba4", foreground="#dce4ee", sticky="nsew")
style.configure("mystyle.Treeview", background="#252524", highlightthickness=0, bd=0, font=('Calibri', 11), fieldbackground="#252524", foreground="#ffb3b3")

student_list = ttk.Treeview(root, columns=("name", "id_num", "course", "year_level", "gpa"), show="headings", style="mystyle.Treeview")
student_list.grid(row=8, column=0, columnspan=5, padx=20, pady=20)
student_list.heading("name", text="Name")
student_list.heading("id_num", text="ID")
student_list.heading("course", text="Course")
student_list.heading("year_level", text="Year Level")
student_list.heading("gpa", text="GPA")

student_list.column("#0", width=0, stretch=tk.NO)
student_list.column("name", width=240, anchor=tk.CENTER)
student_list.column("id_num", width=160, anchor=tk.CENTER)
student_list.column("course", width=200, anchor=tk.CENTER)
student_list.column("year_level", width=180, anchor=tk.CENTER)
student_list.column("gpa", width=100, anchor=tk.CENTER)




retrieve_data()
root.mainloop()
