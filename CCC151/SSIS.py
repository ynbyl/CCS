import tkinter as tk
import tkinter.ttk as ttk
import customtkinter
import subprocess




# Create the main window
root = customtkinter.CTk()
root.title("Student Information System")
root.configure(bg="#2a2d30")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")
button_update_visible = False  # Global variable for 'Update'
selected_index = None  # Declare a global variable to store the index of the selected item
large_font = customtkinter.CTkFont(size=30)



# Class to store and represent student data
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

    # Initializes the variable
    list_data = []
    try:
        # Open the save.txt file for reading
        with open("save.txt", "r", encoding="utf-8") as file:
            for std in file:
                # Splits data
                data = std.strip().split("     ")

                # Insert the student data to student_list
                student_list.insert("", tk.END, values=(data[0], data[1], data[2], data[3], data[4]))

                # Add the student information to the list_data list
                list_data.append(std.strip())
    except:
        pass # Does nothing :D


# Function to retrieve data from "courses.txt" and populate the dropdown menu
def courses(course_entry):
    # Read course values for combobox
    try:
        with open("courses.txt", "r", encoding="utf-8") as file:
            courses = [course.strip() for course in file]
            course_entry['values'] = courses
    except FileNotFoundError:
        print("courses.txt file not found.")


# Function to add student to the list
def add():
    global list_data

    # Take values
    first_name = first_name_entry.get()
    middle_initial = middle_initial_entry.get()
    last_name = last_name_entry.get()
    course = course_entry.get()
    id_num = id_entry.get()
    year_level = year_entry.get()
    gpa = gpa_entry.get()

    # Bug fixing purposes
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

    # To combine the 3 entries into the name column in treeview
    name = f"{first_name} {middle_initial} {last_name}"

    # Insert student data into the treeview
    student = Student(name, id_num, course, year_level, gpa)
    student_info = (student.name, student.id_num, student.course, student.year_level, student.gpa)

    # Add data to list_data
    student_list.insert("", tk.END, values=student_info)
    list_data.append("     ".join(student_info))

    # Clear entry
    first_name_entry.delete(0, 'end')
    middle_initial_entry.delete(0, 'end')
    last_name_entry.delete(0, 'end')
    id_entry.delete(0, 'end')
    course_entry.delete(0, 'end')
    gpa_entry.delete(0, 'end')


# Function to "Edit" or simply replace students :) // Updated into a better version
def edit_selected():
    global selected_index, button_update_visible

    selected_item = student_list.selection()

    if selected_item:
        # Get selected student's data
        values = student_list.item(selected_item)['values']

        # For name
        name = values[0].split(" ")

        # Copy to entry fields
        first_name_entry.insert(0, name[0])
        middle_initial_entry.insert(0, name[1])
        last_name_entry.insert(0, name[2])
        id_entry.insert(0, values[1])
        gpa_entry.insert(0, values[4])

        # Store the index of the selected item
        selected_index = student_list.index(selected_item)

        # Show the "Update" button and hide the "Add Student" button
        if not button_update_visible:
            button_update.grid(row=3, column=4, padx=20, pady=20)
            button.grid_remove()  # Hide the "Add Student" button
            button_update_visible = True

# Insert student
def update_student():
    global selected_index, button_update_visible

    if selected_index is not None:
        # Get the updated data from the entry fields
        first_name = first_name_entry.get()
        middle_initial = middle_initial_entry.get()
        last_name = last_name_entry.get()
        course = course_entry.get()
        id_num = id_entry.get()
        year_level = year_entry.get()
        gpa = gpa_entry.get()

        # Update the selected item with the new data
        name = f"{first_name} {middle_initial} {last_name}"
        student_list.item(student_list.selection(), values=(name, id_num, course, year_level, gpa))

        # Clear the entry fields
        first_name_entry.delete(0, 'end')
        middle_initial_entry.delete(0, 'end')
        last_name_entry.delete(0, 'end')
        id_entry.delete(0, 'end')
        course_entry.delete(0, 'end')
        gpa_entry.delete(0, 'end')

        # Reset the selected_index variable
        selected_index = None

        # Hide the "Update" button and show the "Add Student" button
        if button_update_visible:
            button_update.grid_remove()
            button.grid(row=0, column=4, padx=20, pady=20, rowspan=3)  # Show the "Add Student" button
            button_update_visible = False





# Function to delete ALL students on the list
def delete():
    global list_data

    student_list.delete(*student_list.get_children())
    list_data = []


# Function to delete selected student from the list
def delete_selected():
    selected_item = student_list.selection()

    if selected_item:
        # Get the selected item index
        selected_index = student_list.index(selected_item)
        # Delete the selected item from the student_list
        student_list.delete(selected_item)
        # Update the list_data by removing the selected student
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
    # Get the search query search entry
    search_query = search_entry.get().strip().lower()
    # Searches if there is a filled entry
    if search_query:
        # Take all data
        items = student_list.get_children("")
        # Remove accidental selections
        student_list.selection_remove(*student_list.get_children())

        # Search iterates and checks if the 'entry' matches any value in the list
        for item in items:
            # Get the values associated with the item
            values = student_list.item(item)["values"]
            # Check if the search query matches any value in the values list
            if any(search_query in str(value).lower() for value in values):
                # Add the item to the selection
                student_list.selection_add(item)
                # Focuses then highlights
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
year_entry = customtkinter.CTkComboBox(root, values=["Highschool", "1st Year", "2nd Year", "3rd Year", "4th Year", "Alumni"], state="readonly")
year_entry.grid(row=1, column=3, padx=20, pady=20)

gpa_label = customtkinter.CTkLabel(root, text="GPA:")
gpa_label.grid(row=2, column=2, padx=20, pady=20)
gpa_entry = customtkinter.CTkEntry(root)
gpa_entry.grid(row=2, column=3, padx=20, pady=20)

search_label = customtkinter.CTkLabel(root, text="Search Student")
search_label.grid(row=4, column=1, padx=20, pady=20)
search_entry = customtkinter.CTkEntry(root)
search_entry.grid(row=4, column=2, padx=20, pady=20)




# Button Show
button_update = customtkinter.CTkButton(root, text="Update \n Student", command=update_student, height=100, font=large_font)
button_update.grid(row=3, column=4, padx=20, pady=20, rowspan=2)
button_update.grid_remove()  # Hide the button initially

# Button Search
search_button = customtkinter.CTkButton(root, text="Search", command=search)
search_button.grid(row=4, column=3, padx=20, pady=20)

# Button Add
button = customtkinter.CTkButton(root, text="Add \n \n Student", command=add, height=100, font=large_font)
button.grid(row=0, column=4, padx=20, pady=20, rowspan=3)

# Button Edit
button_edit = customtkinter.CTkButton(root, text="Edit Selected Student", command=edit_selected)
button_edit.grid(row=3, column=3, padx=20, pady=20)

# Button Remove
button_delete_selected = customtkinter.CTkButton(root, text="Remove Selected Student", command=delete_selected)
button_delete_selected.grid(row=3, column=2, padx=20, pady=20)

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
