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
header.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=120, pady=35)


def view_options_popup():
    view_options_popup = tk.Toplevel(root)
    view_options_popup.title("View Options")
    view_options_popup.geometry("500x300")
    view_options_popup.configure(bg="white")
    view_options_popup.resizable(False, False)

    view_options_popup_label = tk.Label(view_options_popup, text="What would you like to view?", font=("Arial", 30), bg="white", fg="dark blue")
    view_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=55, pady=20)

    view_volunteers_button = ttk.Button(view_options_popup, text="Volunteers", style="Blue.TButton", command=lambda: view_volunteers())
    view_volunteers_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    view_universities_button = ttk.Button(view_options_popup, text="Universities", style="Blue.TButton", command=lambda: view_universities())
    view_universities_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    view_roles_button = ttk.Button(view_options_popup, text="Roles", style="Blue.TButton", command=lambda: view_roles())
    view_roles_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    view_artists_button = ttk.Button(view_options_popup, text="Artists", style="Blue.TButton", command=lambda: view_artists())
    view_artists_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")


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

