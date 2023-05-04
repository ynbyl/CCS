import tkinter as tk

root = tk.Tk()
root.title("Student Information System")

class Student:
    def __init__(self, name, id_num, course, year_level, gpa):
        self.name = name
        self.id_num = id_num
        self.course = course
        self.year_level = year_level
        self.gpa = gpa

def retrieve_data():
    global list_data
    list_data = []
    try:
        with open("unsave.txt", "r", encoding="utf-8") as file:
            for f in file:
                listbox.insert(tk.END, f.strip())
                list_data.append(f.strip())
    except:
        pass

def add():
    global list_data
    name = name_entry.get()
    id_num = id_entry.get()
    course = course_entry.get()
    year_level = year_entry.get()
    gpa = gpa_entry.get()

    student = Student(name, id_num, course, year_level, gpa)
    student_info = f"{student.name} - {student.id_num} - {student.course} - {student.year_level} - {student.gpa}"
    listbox.insert(tk.END, student_info)
    list_data.append(student_info)

def edit_selected():
    delete_selected()
    add()

def delete():
    global list_data
    listbox.delete(0, tk.END)
    list_data = []

def delete_selected():
    global list_data

    try:
        index = listbox.curselection()[0]
        selected = list_data[index]
        listbox.delete(tk.ANCHOR)
        list_data.pop(index)
    except:
        pass

def quit():
    global root
    with open("unsave.txt", "w", encoding="utf-8") as file:
        for d in list_data:
            file.write(d + "\n")
    root.destroy()

# Student Information Form
name_label = tk.Label(root, text="Name:")
name_label.pack()

name_entry = tk.Entry(root)
name_entry.pack()

id_label = tk.Label(root, text="ID:")
id_label.pack()

id_entry = tk.Entry(root)
id_entry.pack()

course_label = tk.Label(root, text="Course:")
course_label.pack()

course_entry = tk.Entry(root)
course_entry.pack()

year_label = tk.Label(root, text="Year Level:")
year_label.pack()

year_entry = tk.Entry(root)
year_entry.pack()

gpa_label = tk.Label(root, text="GPA:")
gpa_label.pack()

gpa_entry = tk.Entry(root)
gpa_entry.pack()

button = tk.Button(root, text="Add Student", command=add)
button.pack()

button_edit = tk.Button(text="Edit Selected Student", command=edit_selected)
button_edit.pack()

button_delete = tk.Button(text="Delete All Students", command=delete)
button_delete.pack()

button_delete_selected = tk.Button(text="Delete Selected Student", command=delete_selected)
button_delete_selected.pack()

listbox = tk.Listbox(root)

listbox.pack()

bquit = tk.Button(root, text="Quit and save", command=quit)
bquit.pack()

retrieve_data()
root.mainloop()
