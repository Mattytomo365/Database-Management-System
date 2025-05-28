import tkinter as tk
from tkinter import ttk
from logic import *
from tkcalendar import DateEntry

root = tk.Tk()
root.title("Volunteer Management System")
root.geometry("500x400")
root.configure(bg="white")
root.resizable(False, False)

initialise_database()


style = ttk.Style(root)
style.theme_use("clam")  # Change theme to allow background color changes
style.configure("Blue.TButton",
                background="dark blue",
                foreground="white",
                font=("Helvetica", 20),
                padding=6)

header = tk.Label(root, text="Welcome", font=("Arial", 60), bg="white", fg="dark blue")
header.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=120, pady=35)

# Popup functions

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

    view_universities_button = ttk.Button(view_options_popup, text="Institutions", style="Blue.TButton", command=lambda: view_institutions_popup())
    view_universities_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    view_roles_button = ttk.Button(view_options_popup, text="Roles", style="Blue.TButton", command=lambda: view_roles_popup())
    view_roles_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    view_artists_button = ttk.Button(view_options_popup, text="Artists", style="Blue.TButton", command=lambda: view_artists_popup())
    view_artists_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")


def add_options_popup():  # Can only add role after institutions have been added
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
    edit_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=65, pady=20)

    edit_volunteer_button = ttk.Button(edit_options_popup, text="Volunteer", style="Blue.TButton", command=lambda: edit_volunteer_popup())
    edit_volunteer_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    edit_institution_button = ttk.Button(edit_options_popup, text="Institution", style="Blue.TButton", command=lambda: edit_institution_popup())
    edit_institution_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    edit_role_button = ttk.Button(edit_options_popup, text="Role", style="Blue.TButton", command=lambda: edit_role_popup())
    edit_role_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    edit_artist_button = ttk.Button(edit_options_popup, text="Artist", style="Blue.TButton", command=lambda: edit_artist_popup())
    edit_artist_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

def delete_options_popup():
    delete_options_popup = tk.Toplevel(root)
    delete_options_popup.title("Delete Options")
    delete_options_popup.geometry("500x300")
    delete_options_popup.configure(bg="white")
    delete_options_popup.resizable(False, False)

    delete_options_popup_label = tk.Label(delete_options_popup, text="What would you like to delete?", font=("Arial", 30), bg="white", fg="dark blue")
    delete_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=45, pady=20)

    delete_volunteer_button = ttk.Button(delete_options_popup, text="Volunteer", style="Blue.TButton", command=lambda: delete_volunteer_popup())
    delete_volunteer_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    delete_institution_button = ttk.Button(delete_options_popup, text="Institution", style="Blue.TButton", command=lambda: delete_institution_popup())
    delete_institution_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    delete_role_button = ttk.Button(delete_options_popup, text="Role", style="Blue.TButton", command=lambda: delete_role_popup())
    delete_role_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    delete_artist_button = ttk.Button(delete_options_popup, text="Artist", style="Blue.TButton", command=lambda: delete_artist_popup())
    delete_artist_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

def view_volunteers_popup():
    pass

def view_institutions_popup():
    pass

def view_roles_popup():
    pass

def view_artists_popup():
    pass

def add_volunteer_popup():  # ADD STATUS???
    add_volunteer_popup = tk.Toplevel(root)
    add_volunteer_popup.title("Add Volunteer")
    add_volunteer_popup.geometry("400x550")
    add_volunteer_popup.configure(bg="white")
    add_volunteer_popup.resizable(False, False)

    header = tk.Label(add_volunteer_popup, text= "Add Volunteer", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    name_label = tk.Label(add_volunteer_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.place(x=100, y=100, anchor=tk.CENTER)
    name_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.place(x=250, y=100, anchor=tk.CENTER)

    email_label = tk.Label(add_volunteer_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
    email_label.place(x=100, y=150, anchor=tk.CENTER)
    email_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    email_entry.place(x=250, y=150, anchor=tk.CENTER)

    phone_label = tk.Label(add_volunteer_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
    phone_label.place(x=100, y=200, anchor=tk.CENTER)
    phone_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    phone_entry.place(x=250, y=200, anchor=tk.CENTER)

    type_dropdown_label = tk.Label(add_volunteer_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
    type_dropdown_label.place(x=100, y=250, anchor=tk.CENTER)
    type_var = tk.StringVar(add_volunteer_popup)
    type_chosen = ttk.Combobox(add_volunteer_popup, width=19, textvariable=type_var)
    type_chosen['values'] = ("Student", "Volunteer")
    type_chosen.place(x=250, y=250, anchor=tk.CENTER)

    start_date_label = tk.Label(add_volunteer_popup, text="Start Date", font=('Arial', 15), bg="white", fg="black")
    start_date_label.place(x=100, y=300, anchor=tk.CENTER)
    start_date_chooser = DateEntry(add_volunteer_popup, width=19, background='dark blue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    start_date_chooser.place(x=250, y=300, anchor=tk.CENTER)

    role_dropdown_label = tk.Label(add_volunteer_popup, text="Role", font=('Arial', 15), bg="white", fg="black")
    role_dropdown_label.place(x=100, y=350, anchor=tk.CENTER)
    role_var = tk.StringVar(add_volunteer_popup)
    role_chosen = ttk.Combobox(add_volunteer_popup, width=19, textvariable=role_var)
    role_chosen['values'] = get_role_names() if get_role_names() else ("No Roles Available")
    role_chosen.place(x=250, y=350, anchor=tk.CENTER)

    institution_dropdown_label = tk.Label(add_volunteer_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
    institution_dropdown_label.place(x=100, y=400, anchor=tk.CENTER)
    institution_var = tk.StringVar(add_volunteer_popup)
    institution_chosen = ttk.Combobox(add_volunteer_popup, width=19, textvariable=institution_var)
    institution_chosen['values'] = get_institution_names() if get_institution_names() else ("No Institutions Available")
    institution_chosen.place(x=250, y=400, anchor=tk.CENTER)

    contract_length_label = tk.Label(add_volunteer_popup, text="Contract Length", font=('Arial', 15), bg="white", fg="black")
    contract_length_label.place(x=100, y=450, anchor=tk.CENTER)
    contract_length_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    contract_length_entry.place(x=250, y=450, anchor=tk.CENTER)

    add_volunteer_button = ttk.Button(add_volunteer_popup, text="Add", style="Blue.TButton", command=lambda: [add_volunteer(name_entry.get(), email_entry.get(), phone_entry.get(), type_var.get(), institution_chosen.get(), role_chosen.get(), start_date_chooser.get_date(), contract_length_entry.get()), add_volunteer_popup.destroy()])
    add_volunteer_button.place(x=200, y=500, anchor=tk.CENTER)

def add_institution_popup():
    add_institution_popup = tk.Toplevel(root)
    add_institution_popup.title("Add Institution")
    add_institution_popup.geometry("400x300")
    add_institution_popup.configure(bg="white")
    add_institution_popup.resizable(False, False)

    header = tk.Label(add_institution_popup, text= "Add Institution", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    name_label = tk.Label(add_institution_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.place(x=100, y=100, anchor=tk.CENTER)
    name_entry = tk.Entry(add_institution_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.place(x=250, y=100, anchor=tk.CENTER)

    type_label = tk.Label(add_institution_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
    type_label.place(x=100, y=150, anchor=tk.CENTER)
    type_var = tk.StringVar(add_institution_popup)
    type_chosen = ttk.Combobox(add_institution_popup, width=19, textvariable=type_var)
    type_chosen['values'] = ("University", "College")
    type_chosen.place(x=250, y=150, anchor=tk.CENTER)

    postcode_label = tk.Label(add_institution_popup, text="Postcode", font=('Arial', 15), bg="white", fg="black")
    postcode_label.place(x=100, y=200, anchor=tk.CENTER)
    postcode_entry = tk.Entry(add_institution_popup, font=('Arial', 15), bg="white", fg="black")
    postcode_entry.place(x=250, y=200, anchor=tk.CENTER)

    add_institution_button = ttk.Button(add_institution_popup, text="Add", style="Blue.TButton", command=lambda: [add_institution(name_entry.get(), type_var.get(), postcode_entry.get()), add_institution_popup.destroy()])
    add_institution_button.place(x=200, y=250, anchor=tk.CENTER)

def add_role_popup():
    add_role_popup = tk.Toplevel(root)
    add_role_popup.title("Add Role")
    add_role_popup.geometry("400x400")
    add_role_popup.configure(bg="white")
    add_role_popup.resizable(False, False)

    header = tk.Label(add_role_popup, text= "Add Role", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)

    name_label = tk.Label(add_role_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.place(x=100, y=100, anchor=tk.CENTER)
    name_entry = tk.Entry(add_role_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.place(x=250, y=100, anchor=tk.CENTER)

    description_label = tk.Label(add_role_popup, text="Description", font=('Arial', 15), bg="white", fg="black")
    description_label.place(x=100, y=150, anchor=tk.CENTER)
    description_entry = tk.Entry(add_role_popup, font=('Arial', 15), bg="white", fg="black")
    description_entry.place(x=250, y=150, anchor=tk.CENTER)

    institution_dropdown_label = tk.Label(add_role_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
    institution_dropdown_label.place(x=100, y=200, anchor=tk.CENTER)
    institution_var = tk.StringVar(add_role_popup)
    institution_chosen = ttk.Combobox(add_role_popup, width=19, state="readonly")
    values = get_institution_names() if get_institution_names() else ("No Institutions Available")
    institution_chosen.place(x=250, y=200, anchor=tk.CENTER)

    institutions_label = tk.Label(add_role_popup, text="Select Here:", font=('Arial', 12), bg="white", fg="black")
    institutions_label.place(x=100, y=230, anchor=tk.CENTER)
    institutions = tk.Listbox(add_role_popup, listvariable=institution_var, height=5, width=27, selectmode="multiple", bg="white", fg="black", font=('Arial', 12), exportselection=0, selectforeground="white", selectbackground="dark blue")
    for value in values:
        institutions.insert(tk.END, value)
    institutions.place(x=250, y=260, anchor=tk.CENTER)

    def update_dropdown():
        selected_indices = institutions.curselection()
        selected_values = [institutions.get(i) for i in selected_indices]
        institution_chosen.set(", ".join(selected_values))

    institutions.bind("<<ListboxSelect>>", lambda event: update_dropdown())

    add_institution_button = ttk.Button(add_role_popup, text="Add", style="Blue.TButton", command=lambda: [add_role(name_entry.get(), description_entry.get(), institution_chosen.get()), add_role_popup.destroy()])
    add_institution_button.place(x=200, y=350, anchor=tk.CENTER)

def add_artist_popup(): # ADD STATUS ???
    add_artist_popup = tk.Toplevel(root)
    add_artist_popup.title("Add Artist")
    add_artist_popup.geometry("400x300")
    add_artist_popup.configure(bg="white")
    add_artist_popup.resizable(False, False)

    header = tk.Label(add_artist_popup, text= "Add Artist", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)

    name_label = tk.Label(add_artist_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.place(x=100, y=100, anchor=tk.CENTER)
    name_entry = tk.Entry(add_artist_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.place(x=250, y=100, anchor=tk.CENTER)

    email_label = tk.Label(add_artist_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
    email_label.place(x=100, y=150, anchor=tk.CENTER)
    email_entry = tk.Entry(add_artist_popup, font=('Arial', 15), bg="white", fg="black")
    email_entry.place(x=250, y=150, anchor=tk.CENTER)

    phone_label = tk.Label(add_artist_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
    phone_label.place(x=100, y=200, anchor=tk.CENTER)
    phone_entry = tk.Entry(add_artist_popup, font=('Arial', 15), bg="white", fg="black")
    phone_entry.place(x=250, y=200, anchor=tk.CENTER)

    add_artist_button = ttk.Button(add_artist_popup, text="Add", style="Blue.TButton", command=lambda: [add_artist(name_entry.get(), email_entry.get(), phone_entry.get()), add_artist_popup.destroy()])
    add_artist_button.place(x=200, y=250, anchor=tk.CENTER)

def edit_volunteer_popup():
    edit_volunteer_popup = tk.Toplevel(root)
    edit_volunteer_popup.title("Edit Volunteer")
    edit_volunteer_popup.geometry("400x550")
    edit_volunteer_popup.configure(bg="white")
    edit_volunteer_popup.resizable(False, False)

    header = tk.Label(edit_volunteer_popup, text= "Edit Volunteer", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    name_label = tk.Label(edit_volunteer_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.place(x=100, y=100, anchor=tk.CENTER)
    name_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.place(x=250, y=100, anchor=tk.CENTER)

    email_label = tk.Label(edit_volunteer_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
    email_label.place(x=100, y=150, anchor=tk.CENTER)
    email_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    email_entry.place(x=250, y=150, anchor=tk.CENTER)

    phone_label = tk.Label(edit_volunteer_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
    phone_label.place(x=100, y=200, anchor=tk.CENTER)
    phone_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    phone_entry.place(x=250, y=200, anchor=tk.CENTER)

    type_dropdown_label = tk.Label(edit_volunteer_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
    type_dropdown_label.place(x=100, y=250, anchor=tk.CENTER)
    type_var = tk.StringVar(edit_volunteer_popup)
    type_chosen = ttk.Combobox(edit_volunteer_popup, width=19, textvariable=type_var)
    type_chosen['values'] = ("Student", "Volunteer")
    type_chosen.place(x=250, y=250, anchor=tk.CENTER)

    start_date_label = tk.Label(edit_volunteer_popup, text="Start Date", font=('Arial', 15), bg="white", fg="black")
    start_date_label.place(x=100, y=300, anchor=tk.CENTER)
    start_date_chooser = DateEntry(edit_volunteer_popup, width=19, background='dark blue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    start_date_chooser.place(x=250, y=300, anchor=tk.CENTER)

    role_dropdown_label = tk.Label(edit_volunteer_popup, text="Role", font=('Arial', 15), bg="white", fg="black")
    role_dropdown_label.place(x=100, y=350, anchor=tk.CENTER)
    role_var = tk.StringVar(edit_volunteer_popup)
    role_chosen = ttk.Combobox(edit_volunteer_popup, width=19, textvariable=role_var)
    role_chosen['values'] = get_role_names() if get_role_names() else ("No Roles Available")
    role_chosen.place(x=250, y=350, anchor=tk.CENTER)

    institution_dropdown_label = tk.Label(edit_volunteer_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
    institution_dropdown_label.place(x=100, y=400, anchor=tk.CENTER)
    institution_var = tk.StringVar(edit_volunteer_popup)
    institution_chosen = ttk.Combobox(edit_volunteer_popup, width=19, textvariable=institution_var)
    institution_chosen['values'] = get_institution_names() if get_institution_names() else ("No Institutions Available")
    institution_chosen.place(x=250, y=400, anchor=tk.CENTER)

    contract_length_label = tk.Label(edit_volunteer_popup, text="Contract Length", font=('Arial', 15), bg="white", fg="black")
    contract_length_label.place(x=100, y=450, anchor=tk.CENTER)
    contract_length_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    contract_length_entry.place(x=250, y=450, anchor=tk.CENTER)

    edit_volunteer_button = ttk.Button(edit_volunteer_popup, text="Save", style="Blue.TButton", command=lambda: [edit_volunteer(name_entry.get(), email_entry.get(), phone_entry.get(), type_var.get(), institution_chosen.get(), role_chosen.get(), start_date_chooser.get_date(), contract_length_entry.get()), edit_volunteer_popup.destroy()])
    edit_volunteer_button.place(x=200, y=500, anchor=tk.CENTER)
    

def edit_institution_popup():
    edit_institution_popup = tk.Toplevel(root)
    edit_institution_popup.title("Edit Institution")
    edit_institution_popup.geometry("400x300")
    edit_institution_popup.configure(bg="white")
    edit_institution_popup.resizable(False, False)

    header = tk.Label(edit_institution_popup, text= "Edit Institution", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    name_label = tk.Label(edit_institution_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.place(x=100, y=100, anchor=tk.CENTER)
    name_entry = tk.Entry(edit_institution_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.place(x=250, y=100, anchor=tk.CENTER)

    type_label = tk.Label(edit_institution_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
    type_label.place(x=100, y=150, anchor=tk.CENTER)
    type_var = tk.StringVar(edit_institution_popup)
    type_chosen = ttk.Combobox(edit_institution_popup, width=19, textvariable=type_var)
    type_chosen['values'] = ("University", "College")
    type_chosen.place(x=250, y=150, anchor=tk.CENTER)

    postcode_label = tk.Label(edit_institution_popup, text="Postcode", font=('Arial', 15), bg="white", fg="black")
    postcode_label.place(x=100, y=200, anchor=tk.CENTER)
    postcode_entry = tk.Entry(edit_institution_popup, font=('Arial', 15), bg="white", fg="black")
    postcode_entry.place(x=250, y=200, anchor=tk.CENTER)

    edit_institution_button = ttk.Button(edit_institution_popup, text="Save", style="Blue.TButton", command=lambda: [edit_institution(name_entry.get(), type_var.get(), postcode_entry.get()), edit_institution_popup.destroy()])
    edit_institution_button.place(x=200, y=250, anchor=tk.CENTER)

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

