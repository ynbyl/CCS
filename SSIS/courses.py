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
    file_path = "D:/Downloads/SSIS/courses.txt"
    try:
        with open(file_path, "r", encoding="utf-8") as file:
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


# Function to update course
def upd_selected():
    try:
        index = listbox.curselection()[0]
        selected = list_data[index]
        course_entry.delete(0, 'end')
        course_code_entry.delete(0, 'end')
        course, course_code = selected.split(" | ")
        course_entry.insert(0, course)
        course_code_entry.insert(0, course_code)
    except IndexError:
        pass


# Function to confirm the update of the selected course
def upd_confirmed():
    try:
        index = listbox.curselection()[0]
        selected = list_data[index]
        new_course = course_entry.get()
        new_course_code = course_code_entry.get()
        updated_info = f"{new_course} | {new_course_code}"
        listbox.delete(index)
        listbox.insert(index, updated_info)
        list_data[index] = updated_info
        course_entry.delete(0, 'end')
        course_code_entry.delete(0, 'end')
    except IndexError:
        pass


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
    file_path = "D:/Downloads/SSIS/courses.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        for d in list_data:
            file.write(d + "\n")

    program_path = "D:/Downloads/SSIS/ssis.py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")

    root.destroy()


# Function seasrch for student in all columns
def search():
    # Get the search query from the search entry
    search_query = search_entry.get().strip().lower()
    # Clear previous selections
    listbox.selection_clear(0, tk.END)
    # Searches if there is a filled entry
    if search_query:
        # Take all data
        items = listbox.get(0, tk.END)

        # Search iterates and checks if the 'entry' matches any value in the list
        for i, item in enumerate(items):
            # Get the values associated with the item
            values = item.split(" | ")
            # Check if the search query matches any value in the values list
            if any(search_query in value.lower() for value in values):
                # Add the item to the selection
                listbox.selection_set(i)
                # Focus then highlight
                listbox.focus_set()
                listbox.activate(i)




# Student Information Form
course_label = customtkinter.CTkLabel(root, text="Course Code:")
course_label.grid(row=0, column=0, padx=10, pady=10)
course_entry = customtkinter.CTkEntry(root)
course_entry.grid(row=0, column=1, padx=10, pady=10)

course_code_label = customtkinter.CTkLabel(root, text="Course:")
course_code_label.grid(row=1, column=0, padx=10, pady=10)
course_code_entry = customtkinter.CTkEntry(root)
course_code_entry.grid(row=1, column=1, padx=10, pady=10)

search_label = customtkinter.CTkLabel(root, text="Search:")
search_label.grid(row=8, column=0, padx=10, pady=10)
search_entry = customtkinter.CTkEntry(root)
search_entry.grid(row=8, column=1, padx=10, pady=10)




# Buttons
root.bind('<Return>', add)

button_edit = customtkinter.CTkButton(root, text="Edit Course", command=upd_selected)
button_edit.grid(row=1, column=2, padx=10, pady=10)

button_confirm = customtkinter.CTkButton(root, text="Update Course", command=upd_confirmed)
button_confirm.grid(row=2, column=2, padx=10, pady=10)

button_delete = customtkinter.CTkButton(root, text="Remove All Courses", command=delete)
button_delete.grid(row=2, column=0, padx=10, pady=10)

button_delete_selected = customtkinter.CTkButton(root, text="Remove Selected Course", command=delete_selected)
button_delete_selected.grid(row=2, column=1, padx=10, pady=10)

button_search = customtkinter.CTkButton(root, text="Search Student", command=search)
button_search.grid(row=8, column=2, padx=10, pady=10)

bquit = customtkinter.CTkButton(root, text="Return to Student List", command=quit)
bquit.grid(row=9, column=1, padx=10, pady=10)




# Create the listbox
listbox = tk.Listbox(root)
listbox.grid(row=7, column=0, columnspan=3, padx=1, pady=20)  # Modified grid parameters
listbox.configure(bg="#252524", fg="white")




load_courses()
root.mainloop()