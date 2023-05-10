import subprocess
import tkinter as tk
import customtkinter

# Create the main window
root = customtkinter.CTk()
root.title("Open Program")
root.configure(bg="#2a2d30")
root.resizable(False, False)
customtkinter.set_appearance_mode("Dark")


def open_program():
    program_path = "C:/Users/roelb/PycharmProjects/pythonProject2/courses.py"
    try:
        subprocess.Popen(["python", program_path])
    except FileNotFoundError:
        print("Program file not found.")


# Create a button to open the program
button = customtkinter.CTkButton(root, text="Open Program", command=open_program)
button.pack(padx=10, pady=10)

root.mainloop()
