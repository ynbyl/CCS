import tkinter as tk
import customtkinter



# Create the main window
root = customtkinter.CTk()
root.title("Student Information System")
root.configure(bg="#2a2d30")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


# A class to represent a student and store their information
class Student:
    def __init__(self, name, id_num, course, year_level, gpa):
        self.name = name
        self.id_num = id_num
        self.course = course
        self.year_level = year_level
        self.gpa = gpa

# Function to retrieve data saved when executable was exited
def retrieve_data():
    global list_data
    list_data = []
    try:
        with open("save.txt", "r", encoding="utf-8") as file:
            for f in file:
                listbox.insert(tk.END, f.strip())
                list_data.append(f.strip())
    except:
        pass

# Function to add student to the list
def add():
    global list_data
    name = name_entry.get()
    id_num = id_entry.get()
    course = course_entry.get()
    year_level = year_entry.get()
    gpa = gpa_entry.get()

    student = Student(name, id_num, course, year_level, gpa)
    student_info = f"{student.name}     {student.id_num}     {student.course}     {student.year_level}     {student.gpa}"
    listbox.insert(tk.END, student_info)
    list_data.append(student_info)

# Function to "Edit" or simply replace students
def edit_selected():
    delete_selected()
    add()

# Function to delete ALL of the student lists
def delete():
    global list_data
    listbox.delete(0, tk.END)
    list_data = []
# Function to delete the selected student from the list
def delete_selected():
    global list_data

    try:
        index = listbox.curselection()[0]
        selected = list_data[index]
        listbox.delete(tk.ANCHOR)
        list_data.pop(index)
    except:
        pass

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
course_label.grid(row=3, column=0, padx=10, pady=10)

course_entry = customtkinter.CTkEntry(root)
course_entry.grid(row=3, column=1, padx=10, pady=10)


year_label = customtkinter.CTkLabel(root, text="Year Level:")
year_label.grid(row=2, column=0, padx=10, pady=10)

year_entry = customtkinter.CTkEntry(root)
year_entry.grid(row=2, column=1, padx=10, pady=10)


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

# Create the listbox
listbox = tk.Listbox(root)
listbox.grid(row=7, columnspan=5, sticky="nsew", padx=10, pady=20)
listbox.configure(bg="#252524", fg="white")

# Create a button to Save and Quit
bquit = customtkinter.CTkButton(root, text="Save and Quit", command=quit)
bquit.grid(row=9, column=1, padx=10, pady=10)

retrieve_data()
root.mainloop()
