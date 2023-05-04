import customtkinter

from tkinter import *

# Create the main window
root = customtkinter.CTk()

root.title("Student Information System")
root.configure(bg="#ffb3b3")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")



# Function to add student to the list
def add_student():
    name = name_entry.get()
    id = id_entry.get()
    grade = grade_entry.get()
    student = {'name': name, 'id': id, 'grade': grade}
    students.append(student)
    display_students()


# Function to display students in a text widget
def display_students():
    student_list.delete(0, END)
    for student in students:
        student_list.insert(END, f"Name: {student['name']} | ID: {student['id']} | Grade: {student['grade']}")


# Function to delete the selected student from the list
def delete_student():
    selected_student = student_list.get(student_list.curselection())
    for i, student in enumerate(students):
        if f"Name: {student['name']} | ID: {student['id']} | Grade: {student['grade']}" == selected_student:
            del students[i]
            break
    display_students()






# Create labels and entry fields for student information
name_label = Label(root, text="Name:")
name_label.grid(row=0, column=0)
name_entry = Entry(root)
name_entry.grid(row=0, column=1)

id_label = Label(root, text="ID:")
id_label.grid(row=1, column=0)
id_entry = Entry(root)
id_entry.grid(row=1, column=1)

grade_label = Label(root, text="Year Level:")
grade_label.grid(row=2, column=0)
grade_entry = Entry(root)
grade_entry.grid(row=2, column=1)

# Create a button to add a new student
add_button = Button(root, text="Add Student", command=add_student)
add_button.grid(row=3, column=0, pady=10)

# Create a listbox to display the student information
student_list = Listbox(root, width=40, height=20)
student_list.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# Create a button to delete a selected student
delete_button = Button(root, text="Delete Selected", command=delete_student)
delete_button.grid(row=5, column=0, pady=10)

# Create a button to quit the program
quit_button = Button(root, text="Quit", command=root.quit)
quit_button.grid(row=5, column=1, pady=10)

# Initialize the list of students
students = []

root.mainloop()
