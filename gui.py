import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Volunteer Management System")
root.geometry("500x400")
root.configure(bg="white")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")  # Change theme to allow background color changes
style.configure("Blue.TButton",
                background="dark blue",
                foreground="white",
                font=("Helvetica", 20),
                padding=6)

header = tk.Label(root, text="Welcome", font=("Arial", 60), bg="white", fg="dark blue")
header.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=120, pady=40)


def view_options_popup():
    pass

def add_options_popup():
    pass

def edit_options_popup():
    pass

def delete_options_popup():
    pass

def view_volunteers():
    pass

def view_universities():
    pass

def view_roles():
    pass

def view_artists():
    pass


view_button = ttk.Button(root, text="View", style="Blue.TButton", command=lambda: view_options_popup())
view_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

add_button = ttk.Button(root, text="Add", style="Blue.TButton", command=lambda: add_options_popup())
add_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

edit_button = ttk.Button(root, text="Edit", style="Blue.TButton", command=lambda: edit_options_popup())
edit_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

delete_button = ttk.Button(root, text="Delete", style="Blue.TButton", command=lambda: delete_options_popup())
delete_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

root.mainloop()

