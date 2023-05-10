import tkinter as tk
import tkinter.ttk as ttk
import customtkinter



# Create the main window
root = customtkinter.CTk()
root.title("Student Information System")
root.configure(bg="#2a2d30")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")



# A class to represent a student and store their information
class Student:
    def __init__(self, name, id_num, course, year_level, gpa):
        self.name = name
        self.id_num = id_num
        self.course = course
        self.year_level = year_level
        self.gpa = gpa

# Function to retrieve data saved when exec is exited
def retrieve_data():
    global list_data

    list_data = []

    try:
        with open("save.txt", "r", encoding="utf-8") as file:
            for f in file:
                data = f.strip().split("     ")
                student_list.insert("", tk.END, values=(data[0], data[1], data[2], data[3], data[4]))
                list_data.append(f.strip())
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

    name = name_entry.get().strip() or "-"
    id_num = id_entry.get().strip() or "-"
    course = course_entry.get().strip() or "-"
    year_level = year_entry.get().strip() or "-"
    gpa = gpa_entry.get().strip() or "-"

    student = Student(name, id_num, course, year_level, gpa)
    student_info = (student.name, student.id_num, student.course, student.year_level, student.gpa)
    student_list.insert("", tk.END, values=student_info)
    list_data.append("     ".join(student_info))

# Function to "Edit" or simply replace students
def edit_selected():
    selected_item = student_list.selection()

    if selected_item:
        # Get the selected student's data
        values = student_list.item(selected_item)['values']
        name_entry.delete(0, 'end')
        name_entry.insert(0, values[0])
        id_entry.delete(0, 'end')
        id_entry.insert(0, values[1])
        course_entry.delete(0, 'end')
        course_entry.insert(0, values[2])
        year_entry.delete(0, 'end')
        year_entry.insert(0, values[3])
        gpa_entry.delete(0, 'end')
        gpa_entry.insert(0, values[4])
        delete_selected()

# Function to delete ALL of the student lists
def delete():
    global list_data
    student_list.delete(*student_list.get_children())
    list_data = []

# Function to delete the selected student from the list
def delete_selected():
    global list_data

    selected_item = student_list.selection()

    if selected_item:
        index = int(selected_item[0][1:]) - 1
        student_list.delete(selected_item)
        list_data.pop(index)


# Function to open courses program using subprocess
def open_courses():
    # put the file location here
    program_path = "C:/Users/roelb/PycharmProjects/pythonProject2/courses.py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")

# Function to save the data to a file and exit the program
def quit():
    global root
    with open("save.txt", "w", encoding="utf-8") as file:
        for d in list_data:
            file.write(d + "\n")
    root.destroy()



# Student Information Form
name_label = customtkinter.CTkLabel(root, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=10)

name_entry = customtkinter.CTkEntry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)


id_label = customtkinter.CTkLabel(root, text="ID:")
id_label.grid(row=1, column=0, padx=10, pady=10)

id_entry = customtkinter.CTkEntry(root)
id_entry.grid(row=1, column=1, padx=10, pady=10)


course_label = customtkinter.CTkLabel(root, text="Course:")
course_label.grid(row=2, column=0, padx=10, pady=10)

course_entry = ttk.Combobox(root)
course_entry.grid(row=2, column=1, padx=10, pady=10)

courses(course_entry)


year_label = customtkinter.CTkLabel(root, text="Year Level:")
year_label.grid(row=3, column=0, padx=10, pady=10)

year_entry = customtkinter.CTkEntry(root)
year_entry.grid(row=3, column=1, padx=10, pady=10)


gpa_label = customtkinter.CTkLabel(root, text="GPA:")
gpa_label.grid(row=4, column=0, padx=10, pady=10)

gpa_entry = customtkinter.CTkEntry(root)
gpa_entry.grid(row=4, column=1, padx=10, pady=10)



# Create a button to add a new student
button = customtkinter.CTkButton(root, text="Add Student", command=add)
button.grid(row=2, column=2, padx=10, pady=10)

# Create a button to edit selected
button_edit = customtkinter.CTkButton(root, text="Edit Selected Student", command=edit_selected)
button_edit.grid(row=5, column=1, padx=10, pady=10)

# Create a button to deletes ALL inputs
button_delete = customtkinter.CTkButton(root, text="Remove All Students", command=delete)
button_delete.grid(row=5, column=0, padx=10, pady=10)

# Create a button to delete SELECTED input
button_delete_selected = customtkinter.CTkButton(root, text="Remove Selected Student", command=delete_selected)
button_delete_selected.grid(row=5, column=2, padx=10, pady=10)

# Create a button to open courses application
button_open = customtkinter.CTkButton(root, text="Open Course Selection", command=open_courses)
button_open.grid(row=9, column=0, padx=10, pady=10)

# Create a button to Save and Quit
bquit = customtkinter.CTkButton(root, text="Save and Quit", command=quit)
bquit.grid(row=9, column=1, padx=10, pady=10)



# Create a style
style = ttk.Style()
style.theme_use("default")
style.configure("mystyle.Treeview.Heading", font=('Calibri', 12,'bold'), background="#1f6ba4", foreground="#dce4ee")
style.configure("mystyle.Treeview", background="#252524", highlightthickness=0, bd=0, font=('Calibri', 11), fieldbackground="#252524", foreground="#ffb3b3")

# Create a TreeView to display the student information
student_list = ttk.Treeview(root, columns=("name", "id_num", "course", "year_level", "gpa"), show="headings", style="mystyle.Treeview")
student_list.grid(row=7, column=0, columnspan=3, padx=10, pady=10)
student_list.heading("name", text="Name")
student_list.heading("id_num", text="ID")
student_list.heading("course", text="Course")
student_list.heading("year_level", text="Year Level")
student_list.heading("gpa", text="GPA")
student_list.column("#0", width=0, stretch=tk.NO)
student_list.column("name", width=120, anchor=tk.CENTER)
student_list.column("id_num", width=80, anchor=tk.CENTER)
student_list.column("course", width=120, anchor=tk.CENTER)
student_list.column("year_level", width=80, anchor=tk.CENTER)
student_list.column("gpa", width=60, anchor=tk.CENTER)



retrieve_data()
root.mainloop()