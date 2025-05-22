import tkinter as tk
from tkinter import ttk
from logic import *

root = tk.Tk()
root.title("Volunteer Management System")
root.geometry("500x400")
root.configure(bg="white")
root.resizable(False, False)

create_volunteer_table()
create_institution_table()
create_role_table()
create_artist_table()

style = ttk.Style(root)
style.theme_use("clam")  # Change theme to allow background color changes
style.configure("Blue.TButton",
                background="dark blue",
                foreground="white",
                font=("Helvetica", 20),
                padding=6)

header = tk.Label(root, text="Welcome", font=("Arial", 60), bg="white", fg="dark blue")
header.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=120, pady=35)


def view_options_popup():
    view_options_popup = tk.Toplevel(root)
    view_options_popup.title("View Options")
    view_options_popup.geometry("500x300")
    view_options_popup.configure(bg="white")
    view_options_popup.resizable(False, False)

    view_options_popup_label = tk.Label(view_options_popup, text="What would you like to view?", font=("Arial", 30), bg="white", fg="dark blue")
    view_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=55, pady=20)

    view_volunteers_button = ttk.Button(view_options_popup, text="Volunteers", style="Blue.TButton", command=lambda: view_volunteers_popup())
    view_volunteers_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    view_universities_button = ttk.Button(view_options_popup, text="Institution", style="Blue.TButton", command=lambda: view_institutions_popup())
    view_universities_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    view_roles_button = ttk.Button(view_options_popup, text="Roles", style="Blue.TButton", command=lambda: view_roles_popup())
    view_roles_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    view_artists_button = ttk.Button(view_options_popup, text="Artists", style="Blue.TButton", command=lambda: view_artists_popup())
    view_artists_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")


def add_options_popup():
    add_options_popup = tk.Toplevel(root)
    add_options_popup.title("Add Options")
    add_options_popup.geometry("500x300")
    add_options_popup.configure(bg="white")
    add_options_popup.resizable(False, False)

    add_options_popup_label = tk.Label(add_options_popup, text="What would you like to add?", font=("Arial", 30), bg="white", fg="dark blue")
    add_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=55, pady=20)

    add_volunteer_button = ttk.Button(add_options_popup, text="Volunteer", style="Blue.TButton", command=lambda: add_volunteer_popup())
    add_volunteer_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    add_institution_button = ttk.Button(add_options_popup, text="Institution", style="Blue.TButton", command=lambda: add_institution_popup())
    add_institution_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    add_role_button = ttk.Button(add_options_popup, text="Role", style="Blue.TButton", command=lambda: add_role_popup())
    add_role_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    add_artist_button = ttk.Button(add_options_popup, text="Artist", style="Blue.TButton", command=lambda: add_artist_popup())
    add_artist_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

def edit_options_popup():
    edit_options_popup = tk.Toplevel(root)
    edit_options_popup.title("Edit Options")
    edit_options_popup.geometry("500x300")
    edit_options_popup.configure(bg="white")
    edit_options_popup.resizable(False, False)

    edit_options_popup_label = tk.Label(edit_options_popup, text="What would you like to edit?", font=("Arial", 30), bg="white", fg="dark blue")
    edit_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=55, pady=20)

    edit_volunteer_button = ttk.Button(edit_options_popup, text="Volunteer", style="Blue.TButton", command=lambda: edit_volunteer_popup())
    edit_volunteer_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    edit_institution_button = ttk.Button(edit_options_popup, text="Institution", style="Blue.TButton", command=lambda: edit_institution_popup())
    edit_institution_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    edit_role_button = ttk.Button(edit_options_popup, text="Role", style="Blue.TButton", command=lambda: edit_role_popup())
    edit_role_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    edit_artist_button = ttk.Button(edit_options_popup, text="Artist", style="Blue.TButton", command=lambda: edit_artist_popup())
    edit_artist_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

def delete_options_popup():
    pass

def view_volunteers_popup():
    pass

def view_institutions_popup():
    pass

def view_roles_popup():
    pass

def view_artists_popup():
    pass

def add_volunteer_popup():
    pass

def add_institution_popup():
    pass

def add_role_popup():
    pass

def add_artist_popup():
    pass

def edit_volunteer_popup():
    pass

def edit_institution_popup():
    pass

def edit_role_popup():
    pass

def edit_artist_popup():
    pass

def delete_volunteer_popup():
    pass

def delete_institution_popup():
    pass

def delete_role_popup():
    pass

def delete_artist_popup():
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

