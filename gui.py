import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from logic import *
from tkcalendar import DateEntry
from datetime import datetime

initialise_database() # Creates tables in database schema if they don't already exist

root = tk.Tk()
root.title("Database Management System")
root.geometry("570x400")
root.configure(bg="white")
root.resizable(False, False)

style = ttk.Style(root)
style.theme_use("clam")  # Change theme to allow background color changes
style.configure("Blue.TButton",
                background="dark blue",
                foreground="white",
                font=("Helvetica", 20),
                padding=6)

'''Validation Functions'''

def entry_validation(**kwargs):
    for entry_name, entry_value in kwargs.items():
        if entry_value == "":
            messagebox.showinfo(title='Error', message=f'{entry_name} must be filled')
            return False
    return True

def dropdown_validation(dropdowns):
    for dropdown_name, dropdown_value, dropdown_values in dropdowns:
        if dropdown_value == "":
            messagebox.showinfo(title='Error', message=f'{dropdown_name} must be selected')
            return False

        elif dropdown_value != "" and dropdown_value not in dropdown_values:
            messagebox.showinfo(title='Error', message=f'Invalid value in {dropdown_name} dropdown')
            return False
    return True


def date_validation(date):
    if not datetime.strptime(str(date), "%Y-%m-%d"):
        messagebox.showinfo(title='Error', message='Date is invalid')
        return False
    else:
        return True
    
def listbox_validation(role_id, selected_institutions):
    if selected_institutions == "":
        messagebox.showinfo(title='Error', message='No institutions were selected')
        return False
    elif not edit_role_eligibility(role_id, selected_institutions):
        messagebox.showinfo(title='Error', message='Unable to remove institutions that have students with this role')
        return False
    return True

def on_volunteer_submit(volunteer_id, name, email, phone, type_dropdown, institution_dropdown, role_dropdown, start_date, attending_days, contract_length, status_dropdown, badge_number, project, submit_type, popup):
    valid = True
    type = type_dropdown.get()
    institution = institution_dropdown.get()
    role = role_dropdown.get()
    status = status_dropdown.get()

    if not entry_validation(name=name, email=email, phone=phone, attending_days=attending_days, contract_length=contract_length):
        valid = False
    
    if type_dropdown.get() == 'Student':
        if not dropdown_validation([('Type', type, type_dropdown['values']), ('Institution', institution, institution_dropdown['values']), ('Role', role, role_dropdown['values']), ('Status', status, status_dropdown['values'])]):
            valid = False
    else:
        if not dropdown_validation([('Type', type, type_dropdown['values']), ('Role', role, role_dropdown['values']), ('Status', status, status_dropdown['values'])]):
            valid = False
    
    if not date_validation(start_date):
        valid = False
    
    if valid:
        if submit_type == 'Add':
            add_volunteer(name, email, phone, type, institution, role, start_date, attending_days, contract_length, status, badge_number, project)
            popup.destroy()
        elif submit_type == 'Edit':
            edit_volunteer(volunteer_id, name, email, phone, type, institution, role, start_date, attending_days, contract_length, status, badge_number, project)
            popup.destroy()

def on_institution_submit(institution_id, name, type_dropdown, postcode, submit_type, popup):
    valid = True
    type = type_dropdown.get()

    if not entry_validation(name=name, postcode=postcode):
        valid = False
    
    if not dropdown_validation([('Type', type, type_dropdown['values'])]):
        valid = False
    
    if valid:
        if submit_type == 'Add':
            add_institution(name, type, postcode)
            popup.destroy()
        elif submit_type == 'Edit':
            edit_institution(institution_id, name, type, postcode)
            popup.destroy()

def on_role_submit(role_id, name, description, institutions_listbox, submit_type, popup):
    valid = True

    if not entry_validation(name=name, description=description):
        valid = False

    selected_values = [institutions_listbox.get(i) for i in (institutions_listbox.curselection())]
    institution_names = (", ".join(selected_values))

    if not listbox_validation(role_id, institution_names):
        valid = False

    if valid:
        if submit_type == 'Add':
            add_role(name, description, institution_names)
            popup.destroy()
        elif submit_type == 'Edit':
            edit_role(role_id, name, description, institution_names)
            popup.destroy()

def on_artist_submit(artist_id, name, email, phone, submit_type, popup):
    valid = True

    if not entry_validation(name=name, email=email, phone=phone):
        valid = False
    
    if valid:
        if submit_type == 'Add':
            add_artist(name, email, phone)
            popup.destroy()
        elif submit_type == 'Edit':
            edit_artist(artist_id, name, email, phone)
            popup.destroy()


def on_type_select(selected, is_volunteer, type_dropdown, institution_dropdown, role_dropdown, contract_length):
    type = type_dropdown.get()
    institution_dropdown.set("")
    role_dropdown.set("")
    contract_length.set("")
    institution_dropdown.configure(state='disabled' if type == "Volunteer" else 'normal')

    if is_volunteer:
        role_dropdown.set("Volunteer")
        role_dropdown['values'] = ("Volunteer")
        contract_length.set("Indefinite")
    

def on_institution_select(selected, is_volunteer, institution_dropdown, role_dropdown):
    institution = institution_dropdown.get()
    role_dropdown.insert(0, str(" "))
    if not is_volunteer:
        role_dropdown['values'] = get_filtered_role_names(institution) if get_filtered_role_names(institution) else ("No Roles Available")

def on_status_select(selected, status_dropdown, badge_number_entry, project_entry):
    status = status_dropdown.get()
    badge_number_entry.configure(state='normal' if status in ['Awaiting Badge', 'Badged'] else 'disabled')
    project_entry.configure(state='normal' if status in ['Awaiting Badge', 'Badged'] else 'disabled')

'''Options Popups'''

def view_options_popup():
    view_options_popup = tk.Toplevel(root)
    view_options_popup.title("View Options")
    view_options_popup.geometry("600x330")
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


def add_options_popup():
    add_options_popup = tk.Toplevel(root)
    add_options_popup.title("Add Options")
    add_options_popup.geometry("600x330")
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
    add_options_popup.protocol("WM_DELETE_WINDOW", root.deiconify())
    

def edit_options_popup():
    edit_options_popup = tk.Toplevel(root)
    edit_options_popup.title("Edit Options")
    edit_options_popup.geometry("600x330")
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
    delete_options_popup.geometry("600x330")
    delete_options_popup.configure(bg="white")
    delete_options_popup.resizable(False, False)

    delete_options_popup_label = tk.Label(delete_options_popup, text="What would you like to delete?", font=("Arial", 30), bg="white", fg="dark blue")
    delete_options_popup_label.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=35, pady=20)

    delete_volunteer_button = ttk.Button(delete_options_popup, text="Volunteer", style="Blue.TButton", command=lambda: delete_volunteer_popup())
    delete_volunteer_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    delete_institution_button = ttk.Button(delete_options_popup, text="Institution", style="Blue.TButton", command=lambda: delete_institution_popup())
    delete_institution_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

    delete_role_button = ttk.Button(delete_options_popup, text="Role", style="Blue.TButton", command=lambda: delete_role_popup())
    delete_role_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

    delete_artist_button = ttk.Button(delete_options_popup, text="Artist", style="Blue.TButton", command=lambda: delete_artist_popup())
    delete_artist_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

'''Viewing Popups'''

def view_volunteers_popup():

    def filtered_volunteers(selected):
        type = volunteer_filter.get()
        volunteers_filtered = get_filtered_volunteers(type)
        volunteer_table(volunteers_filtered)

    view_volunteers_popup = tk.Toplevel(root)
    view_volunteers_popup.title("View Volunteers")
    view_volunteers_popup.geometry("905x440")
    view_volunteers_popup.configure(bg="white")
    view_volunteers_popup.resizable(False, False)

    view_volunteers_popup_label = tk.Label(view_volunteers_popup, text="View Volunteers", font=("Arial", 30), bg="white", fg="dark blue")
    view_volunteers_popup_label.grid(row=0, column=0, sticky="ew", padx=300, pady=20, columnspan=2)

    volunteer_filter_label = tk.Label(view_volunteers_popup, text="Filter", font=('Arial', 15), bg='white', fg='black')
    volunteer_filter_label.grid(row=1, column=0, sticky='e')
    type_var = tk.StringVar(view_volunteers_popup)
    volunteer_filter = ttk.Combobox(view_volunteers_popup, width=20, textvariable=type_var, state='readonly')
    volunteer_filter['values'] = ("Student", "Volunteer")
    volunteer_filter.grid(row=1, column=1, sticky='w')
    volunteer_filter.bind("<<ComboboxSelected>>", filtered_volunteers)

    canvas = tk.Canvas(view_volunteers_popup, height=300)
    canvas.grid(row=2, column=0, sticky='nsew', columnspan=2)

    h_scroll = tk.Scrollbar(view_volunteers_popup, orient="horizontal", command=canvas.xview)
    h_scroll.grid(row=3, column=0, sticky='ew', columnspan=2)
    canvas.configure(xscrollcommand=h_scroll.set)

    v_scroll = tk.Scrollbar(view_volunteers_popup, orient="vertical", command=canvas.yview)
    v_scroll.grid(row=2, column=2, sticky='ns')
    canvas.configure(yscrollcommand=v_scroll.set)

    volunteer_data = tk.Frame(canvas, bg='dark blue')
    canvas.create_window((0,0), window=volunteer_data, anchor='nw')

    volunteer_data.grid_rowconfigure(0, weight=5)

    def volunteer_table(volunteers):
        nonlocal volunteer_data
        volunteer_data.destroy()
        volunteer_data = tk.Frame(canvas, bg='dark blue')
        canvas.create_window((0,0), window=volunteer_data, anchor='nw')
        volunteer_data.grid_rowconfigure(0, weight=5)

        columns = ["ID", "Name", "E-Mail", "Phone", "Type", "Institution", "Role", "Start Date", "Attending Days", "Contract Length", "Status", "Badge Number", "Project"]
        column_widths = [3, 30, 25, 15, 12, 35, 25, 15, 45, 20, 25, 15, 50]

        for col_index, col_name in enumerate(columns):
            headers = tk.Label(volunteer_data, text=col_name, bg="dark blue", fg="white")
            headers.grid(row=0, column=col_index)

        for row_index, volunteer in enumerate(volunteers):
            if volunteer[4] == 'Student':
                institution_id = volunteer[5]
                role_id = volunteer[6]
                institution_name = get_institution_name(institution_id)
                role_name = get_role_name(role_id)
            else:
                role_name = "Volunteer"
                institution_name = "N/A"
            for col_index, value in enumerate(volunteer):
                information = tk.Entry(volunteer_data, width=column_widths[col_index], bg="white", fg="black")
                information.grid(row=row_index + 3, column=col_index)

                if col_index == 5:
                    display_value = institution_name

                elif col_index == 6:

                    display_value = role_name
                else:
                    display_value = value

                information.insert(0, str(display_value))
                information.configure(state="disabled")

        # Update scrollregion to include the full width of the inner frame
        volunteer_data.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    volunteers = get_volunteers()
    volunteer_table(volunteers)


def view_institutions_popup():

    def filtered_institutions(selected):
        type = institution_filter.get()
        institutions_filtered = get_filtered_institutions(type)
        institutions_table(institutions_filtered)

    view_institutions_popup = tk.Toplevel(root)
    view_institutions_popup.title("View Institutions")
    view_institutions_popup.geometry("400x330")
    view_institutions_popup.configure(bg="white")
    view_institutions_popup.resizable(False, False)

    view_institutions_popup_label = tk.Label(view_institutions_popup, text="View Institutions", font=("Arial", 30), bg="white", fg="dark blue")
    view_institutions_popup_label.grid(row=0, column=0, sticky="ew", padx=0, pady=20, columnspan=2)

    institution_filter_label = tk.Label(view_institutions_popup, text="Filter", font=('Arial', 15), bg='white', fg='black')
    institution_filter_label.grid(row=1, column=0, sticky='e')
    type_var = tk.StringVar(view_institutions_popup)
    institution_filter = ttk.Combobox(view_institutions_popup, width=20, textvariable=type_var, state='readonly')
    institution_filter['values'] = ("University", "College")
    institution_filter.grid(row=1, column=1, sticky='w')
    institution_filter.bind("<<ComboboxSelected>>", filtered_institutions)

    canvas = tk.Canvas(view_institutions_popup, height=205)
    canvas.grid(row=2, column=0, sticky='nsew', columnspan=2)

    v_scroll = tk.Scrollbar(view_institutions_popup, orient="vertical", command=canvas.yview)
    v_scroll.grid(row=2, column=2, sticky='ns')
    canvas.configure(yscrollcommand=v_scroll.set)

    institution_data = tk.Frame(canvas, bg='dark blue')
    canvas.create_window((0,0), window=institution_data, anchor='nw')

    institution_data.grid_rowconfigure(0, weight=5)

    def institutions_table(institutions):

        nonlocal institution_data
        institution_data.destroy()
        institution_data = tk.Frame(canvas, bg='dark blue')
        canvas.create_window((0,0), window=institution_data, anchor='nw')
        institution_data.grid_rowconfigure(0, weight=5)

        columns = ["ID", "Name", "Type", "Postcode"]
        column_widths = [3, 30, 15, 15]

        for col_index, col_name in enumerate(columns):
            headers = tk.Label(institution_data, text=col_name, bg="dark blue", fg="white")
            headers.grid(row=0, column=col_index)

        for row_index, institution in enumerate(institutions):
            for col_index, value in enumerate(institution):
                information = tk.Entry(institution_data, width=column_widths[col_index], bg="white", fg="black")
                information.grid(row=row_index + 3, column=col_index)
                information.insert(0, str(value))
                information.configure(state="disabled")

        institution_data.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    institutions = get_institutions()
    institutions_table(institutions)

def view_roles_popup():

    def filtered_roles(selected):
        institution = role_filter.get()
        roles_filtered = get_filtered_roles(institution)
        roles_table(roles_filtered)

    view_roles_popup = tk.Toplevel(root)
    view_roles_popup.title("View Roles")
    view_roles_popup.geometry("520x330")
    view_roles_popup.configure(bg="white")
    view_roles_popup.resizable(False, False)

    view_roles_popup_label = tk.Label(view_roles_popup, text="View Roles", font=("Arial", 30), bg="white", fg="dark blue")
    view_roles_popup_label.grid(row=0, column=0, sticky="ew", padx=0, pady=20, columnspan=2)

    role_filter_label = tk.Label(view_roles_popup, text="Filter", font=('Arial', 15), bg='white', fg='black')
    role_filter_label.grid(row=1, column=0, sticky='e')
    institution_var = tk.StringVar(view_roles_popup)
    role_filter = ttk.Combobox(view_roles_popup, width=20, textvariable=institution_var, state='readonly')
    role_filter['values'] = get_institution_names() if get_institution_names() else ("No Institutions Available")
    role_filter.grid(row=1, column=1, sticky='w')
    role_filter.bind("<<ComboboxSelected>>", filtered_roles)

    canvas = tk.Canvas(view_roles_popup, height=205, width=500)
    canvas.grid(row=2, column=0, sticky='nsew', columnspan=2)

    v_scroll = tk.Scrollbar(view_roles_popup, orient="vertical", command=canvas.yview)
    v_scroll.grid(row=2, column=2, sticky='ns')
    canvas.configure(yscrollcommand=v_scroll.set)

    role_data = tk.Frame(canvas, bg='dark blue')
    canvas.create_window((0,0), window=role_data, anchor='nw')

    role_data.grid_rowconfigure(0, weight=5)

    def roles_table(roles):
        nonlocal role_data
        role_data.destroy()
        role_data = tk.Frame(canvas, bg='dark blue')
        canvas.create_window((0,0), window=role_data, anchor='nw')
        role_data.grid_rowconfigure(0, weight=5)

        columns = ["ID", "Name", "Description"]
        column_widths = [3, 30, 50]

        for col_index, col_name in enumerate(columns):
            headers = tk.Label(role_data, text=col_name, bg="dark blue", fg="white")
            headers.grid(row=0, column=col_index)

        for row_index, role in enumerate(roles):
            for col_index, value in enumerate(role):
                information = tk.Entry(role_data, width=column_widths[col_index], bg="white", fg="black")
                information.grid(row=row_index + 3, column=col_index)
                information.insert(0, str(value))
                information.configure(state="disabled")

        role_data.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    roles = get_roles()
    roles_table(roles)

def view_artists_popup():
    view_artists_popup = tk.Toplevel(root)
    view_artists_popup.title("View Artists")
    view_artists_popup.geometry("500x300")
    view_artists_popup.configure(bg="white")
    view_artists_popup.resizable(False, False)

    artists = get_artists()

    view_artists_popup_label = tk.Label(view_artists_popup, text="View Artists", font=("Arial", 30), bg="white", fg="dark blue")
    view_artists_popup_label.grid(row=0, column=0, sticky="ew", padx=0, pady=20)

    canvas = tk.Canvas(view_artists_popup, height=205, width=480)
    canvas.grid(row=1, column=0, sticky='nsew')

    v_scroll = tk.Scrollbar(view_artists_popup, orient="vertical", command=canvas.yview)
    v_scroll.grid(row=1, column=1, sticky='ns')
    canvas.configure(yscrollcommand=v_scroll.set)

    artist_data = tk.Frame(canvas, bg='dark blue')
    canvas.create_window((0,0), window=artist_data, anchor='nw')

    artist_data.grid_rowconfigure(0, weight=5)

    columns = ["ID", "Name", "E-Mail", "Phone"]
    column_widths = [3, 30, 30, 15]

    for col_index, col_name in enumerate(columns):
        headers = tk.Label(artist_data, text=col_name, bg="dark blue", fg="white")
        headers.grid(row=0, column=col_index)

    for row_index, artist in enumerate(artists):
        for col_index, value in enumerate(artist):
            information = tk.Entry(artist_data, width=column_widths[col_index], bg="white", fg="black")
            information.grid(row=row_index + 1, column=col_index)
            information.insert(0, str(value))
            information.configure(state="disabled")

    artist_data.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

'''Adding Popups'''

def add_volunteer_popup():
    add_volunteer_popup = tk.Toplevel(root)
    add_volunteer_popup.title("Add Volunteer")
    add_volunteer_popup.geometry("800x450")
    add_volunteer_popup.configure(bg="white")
    add_volunteer_popup.resizable(False, False)

    header = tk.Label(add_volunteer_popup, text= "Add Volunteer", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=270, pady=10, columnspan=5)

    name_label = tk.Label(add_volunteer_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.grid(row=1, column=0, pady=10)
    name_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.grid(row=1, column=1, pady=10, sticky='w')

    email_label = tk.Label(add_volunteer_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
    email_label.grid(row=2, column=0, pady=10)
    email_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    email_entry.grid(row=2, column=1, pady=10, sticky='w')

    phone_label = tk.Label(add_volunteer_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
    phone_label.grid(row=3, column=0, pady=10)
    phone_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    phone_entry.grid(row=3, column=1, pady=10, sticky='w')

    start_date_label = tk.Label(add_volunteer_popup, text="Start Date", font=('Arial', 15), bg="white", fg="black")
    start_date_label.grid(row=4, column=0, pady=10)
    start_date_chooser = DateEntry(add_volunteer_popup, width=34, background='dark blue', foreground='white', borderwidth=2, date_pattern='dd-mm-yyyy')
    start_date_chooser.grid(row=4, column=1, pady=10, sticky='w')

    type_dropdown_label = tk.Label(add_volunteer_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
    type_dropdown_label.grid(row=5, column=0, pady=10)
    type_var = tk.StringVar(add_volunteer_popup)
    type_dropdown = ttk.Combobox(add_volunteer_popup, width=34, textvariable=type_var, state='readonly')
    type_dropdown['values'] = ("Student", "Volunteer")
    type_dropdown.grid(row=5, column=1, pady=10, sticky='w')
    
    institution_dropdown_label = tk.Label(add_volunteer_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
    institution_dropdown_label.grid(row=6, column=0, pady=10)
    institution_var = tk.StringVar(add_volunteer_popup)
    institution_dropdown = ttk.Combobox(add_volunteer_popup, width=34, textvariable=institution_var)
    institution_dropdown['values'] = get_institution_names() if get_institution_names() else ("No Institutions Available")
    institution_dropdown.grid(row=6, column=1, pady=10, sticky='w')

    role_dropdown_label = tk.Label(add_volunteer_popup, text="Role", font=('Arial', 15), bg="white", fg="black")
    role_dropdown_label.grid(row=1, column=3, pady=10)
    role_var = tk.StringVar(add_volunteer_popup)
    role_dropdown = ttk.Combobox(add_volunteer_popup, width=34, textvariable=role_var)
    role_dropdown.grid(row=1, column=4, pady=10, sticky='w')

    attending_days_label = tk.Label(add_volunteer_popup, text="Attending Days", font=('Arial', 15), bg="white", fg="black")
    attending_days_label.grid(row=2, column=3, pady=10)
    attending_days_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
    attending_days_entry.grid(row=2, column=4, pady=10, sticky='w')

    contract_length_label = tk.Label(add_volunteer_popup, text="Contract Length", font=('Arial', 15), bg="white", fg="black")
    contract_length_label.grid(row=3, column=3, pady=10)
    contract_length = tk.StringVar(add_volunteer_popup)
    contract_length_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black", textvariable=contract_length)
    contract_length_entry.grid(row=3, column=4, pady=10, sticky='w')

    status_dropdown_label = tk.Label(add_volunteer_popup, text="Status", font=('Arial', 15), bg="white", fg="black")
    status_dropdown_label.grid(row=4, column=3, pady=10)
    status_var = tk.StringVar(add_volunteer_popup)
    status_dropdown = ttk.Combobox(add_volunteer_popup, width=34, textvariable=status_var, state='readonly')
    status_dropdown['values'] = ("Signing Forms", "Ready to Start", "Awaiting Badge", "Badged")
    status_dropdown.grid(row=4, column=4, pady=10, sticky='w')

    badge_number_label = tk.Label(add_volunteer_popup, text="Badge Number", font=('Arial', 15), bg="white", fg="black")
    badge_number_label.grid(row=5, column=3, pady=10)
    badge_number_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black", state='disabled')
    badge_number_entry.grid(row=5, column=4, pady=10, sticky='w')

    project_label = tk.Label(add_volunteer_popup, text="Project", font=('Arial', 15), bg="white", fg="black")
    project_label.grid(row=6, column=3, pady=10)
    project_entry = tk.Entry(add_volunteer_popup, font=('Arial', 15), bg="white", fg="black", state='disabled')
    project_entry.grid(row=6, column=4, pady=10, sticky='w')


    type_dropdown.bind("<<ComboboxSelected>>", lambda selected: on_type_select(selected, False, type_dropdown, institution_dropdown, role_dropdown, contract_length) if type_dropdown.get() == "Student" else on_type_select(selected, True, type_dropdown, institution_dropdown, role_dropdown, contract_length))

    institution_dropdown.bind("<<ComboboxSelected>>", lambda selected: on_institution_select(selected, False, institution_dropdown, role_dropdown) if type_dropdown.get() == "Student" else on_institution_select(selected, True, institution_dropdown, role_dropdown))

    status_dropdown.bind("<<ComboboxSelected>>", lambda selected: on_status_select(selected, status_dropdown, badge_number_entry, project_entry))

    add_volunteer_button = ttk.Button(add_volunteer_popup, text="Add", style="Blue.TButton", command=lambda: on_volunteer_submit(None, name_entry.get(), email_entry.get(), phone_entry.get(), type_dropdown, institution_dropdown, role_dropdown, start_date_chooser.get_date(), attending_days_entry.get(), contract_length_entry.get(), status_dropdown, badge_number_entry.get(), project_entry.get(), 'Add', add_volunteer_popup))                                                                                               
    add_volunteer_button.grid(row=7, column=0, pady=10, columnspan=5)


def add_institution_popup():
    add_institution_popup = tk.Toplevel(root)
    add_institution_popup.title("Add Institution")
    add_institution_popup.geometry("470x300")
    add_institution_popup.configure(bg="white")
    add_institution_popup.resizable(False, False)

    header = tk.Label(add_institution_popup, text= "Add Institution", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    name_label = tk.Label(add_institution_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.grid(row=1, column=0, pady=10)
    name_entry = tk.Entry(add_institution_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.grid(row=1, column=1, pady=10, sticky='w')

    type_dropdown_label = tk.Label(add_institution_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
    type_dropdown_label.grid(row=2, column=0, pady=10)
    type_var = tk.StringVar(add_institution_popup)
    type_dropdown = ttk.Combobox(add_institution_popup, width=34, textvariable=type_var, state='readonly')
    type_dropdown['values'] = ("University", "College")
    type_dropdown.grid(row=2, column=1, pady=10, sticky='w')

    postcode_label = tk.Label(add_institution_popup, text="Postcode", font=('Arial', 15), bg="white", fg="black")
    postcode_label.grid(row=3, column=0, pady=10)
    postcode_entry = tk.Entry(add_institution_popup, font=('Arial', 15), bg="white", fg="black")
    postcode_entry.grid(row=3, column=1, pady=10, sticky='w')

    add_institution_button = ttk.Button(add_institution_popup, text="Add", style="Blue.TButton", command=lambda: on_institution_submit(None, name_entry.get(), type_dropdown, postcode_entry.get(), 'Add', add_institution_popup))
    add_institution_button.grid(row=4, column=0, pady=10, columnspan=2)

def add_role_popup():
    add_role_popup = tk.Toplevel(root)
    add_role_popup.title("Add Role")
    add_role_popup.geometry("470x400")
    add_role_popup.configure(bg="white")
    add_role_popup.resizable(False, False)

    header = tk.Label(add_role_popup, text= "Add Role", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)

    name_label = tk.Label(add_role_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.grid(row=1, column=0, pady=10)
    name_entry = tk.Entry(add_role_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.grid(row=1, column=1, pady=10, sticky='w')

    description_label = tk.Label(add_role_popup, text="Description", font=('Arial', 15), bg="white", fg="black")
    description_label.grid(row=2, column=0, pady=10)
    description_entry = tk.Entry(add_role_popup, font=('Arial', 15), bg="white", fg="black")
    description_entry.grid(row=2, column=1, pady=10, sticky='w')


    institution_var = tk.StringVar(add_role_popup)
    values = get_institution_names() if get_institution_names() else ("No Institutions Available")
    institutions_label = tk.Label(add_role_popup, text="Select Institutions:", font=('Arial', 12), bg="white", fg="black")
    institutions_label.grid(row=3, column=0, pady=10, sticky='n')
    institutions = tk.Listbox(add_role_popup, listvariable=institution_var, height=5, width=27, selectmode="multiple", bg="white", fg="black", font=('Arial', 12), exportselection=0, selectforeground="white", selectbackground="dark blue")
    for value in values:
        institutions.insert(tk.END, value)
    institutions.grid(row=3, column=1, pady=10, sticky='w')

    add_role_button = ttk.Button(add_role_popup, text="Add", style="Blue.TButton", command=lambda: on_role_submit(None, name_entry.get(), description_entry.get(), institutions, "Add", add_role_popup))
    add_role_button.grid(row=4, column=0, pady=10, columnspan=2)

def add_artist_popup():
    add_artist_popup = tk.Toplevel(root)
    add_artist_popup.title("Add Artist")
    add_artist_popup.geometry("470x300")
    add_artist_popup.configure(bg="white")
    add_artist_popup.resizable(False, False)

    header = tk.Label(add_artist_popup, text= "Add Artist", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)

    name_label = tk.Label(add_artist_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
    name_label.grid(row=1, column=0, pady=10)
    name_entry = tk.Entry(add_artist_popup, font=('Arial', 15), bg="white", fg="black")
    name_entry.grid(row=1, column=1, pady=10, sticky='w')

    email_label = tk.Label(add_artist_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
    email_label.grid(row=2, column=0, pady=10)
    email_entry = tk.Entry(add_artist_popup, font=('Arial', 15), bg="white", fg="black")
    email_entry.grid(row=2, column=1, pady=10, sticky='w')

    phone_label = tk.Label(add_artist_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
    phone_label.grid(row=3, column=0, pady=10)
    phone_entry = tk.Entry(add_artist_popup, font=('Arial', 15), bg="white", fg="black")
    phone_entry.grid(row=3, column=1, pady=10, sticky='w')

    add_artist_button = ttk.Button(add_artist_popup, text="Add", style="Blue.TButton", command=lambda: on_artist_submit(None, name_entry.get(), email_entry.get(), phone_entry.get(), "Add", add_artist_popup))
    add_artist_button.place(x=230, y=250, anchor=tk.CENTER)

'''Editing Popups'''    

def edit_volunteer_popup():
    edit_volunteer_popup = tk.Toplevel(root)
    edit_volunteer_popup.title("Edit Volunteer")
    edit_volunteer_popup.geometry("800x500")
    edit_volunteer_popup.configure(bg="white")
    edit_volunteer_popup.resizable(False, False)

    def edit_volunteer_popup_specific(selected):
        volunteer_details = get_volunteer(volunteer_dropdown.get())
        name_label = tk.Label(edit_volunteer_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
        name_label.grid(row=2, column=0, pady= 10)
        name_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
        name_entry.insert(0, str(volunteer_details[1]))
        name_entry.grid(row=2, column=1, pady=10, sticky='w')

        email_label = tk.Label(edit_volunteer_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
        email_label.grid(row=3, column=0, pady=10)
        email_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
        email_entry.insert(0, str(volunteer_details[2]))
        email_entry.grid(row=3, column=1, pady=10, sticky='w')

        phone_label = tk.Label(edit_volunteer_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
        phone_label.grid(row=4, column=0, pady=10)
        phone_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
        phone_entry.insert(0, str(volunteer_details[3]))
        phone_entry.grid(row=4, column=1, pady=10, sticky='w')

        start_date_label = tk.Label(edit_volunteer_popup, text="Start Date", font=('Arial', 15), bg="white", fg="black")
        start_date_label.grid(row=5, column=0, pady=10)
        start_date_chooser = DateEntry(edit_volunteer_popup, width=34, background='dark blue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        start_date_chooser.delete(0, "end")
        start_date_chooser.set_date(volunteer_details[7])
        start_date_chooser.grid(row=5, column=1, pady=10, sticky='w')

        type_dropdown_label = tk.Label(edit_volunteer_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
        type_dropdown_label.grid(row=6, column=0, pady=10)
        type_var = tk.StringVar(edit_volunteer_popup)
        type_dropdown = ttk.Combobox(edit_volunteer_popup, width=34, textvariable=type_var)
        type_dropdown['values'] = ("Student", "Volunteer")
        type = volunteer_details[4]
        type_dropdown.insert(0, type)
        type_dropdown.grid(row=6, column=1, pady=10, sticky='w')

        institution_dropdown_label = tk.Label(edit_volunteer_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
        institution_dropdown_label.grid(row=7, column=0, pady=10)
        institution_var = tk.StringVar(edit_volunteer_popup)
        institution_dropdown = ttk.Combobox(edit_volunteer_popup, width=34, textvariable=institution_var, state='disabled' if type == "Volunteer" else 'normal')
        institution_dropdown['values'] = get_institution_names() if get_institution_names() else ("No Institutions Available")
        institution_name = get_institution_name(volunteer_details[5])
        institution_dropdown.insert(0, institution_name)
        institution_dropdown.grid(row=7, column=1, pady=10, sticky='w')

        role_dropdown_label = tk.Label(edit_volunteer_popup, text="Role", font=('Arial', 15), bg="white", fg="black")
        role_dropdown_label.grid(row=2, column=3, pady=10)
        role_var = tk.StringVar(edit_volunteer_popup)
        role_dropdown = ttk.Combobox(edit_volunteer_popup, width=34, textvariable=role_var)
        role_name = get_role_name(volunteer_details[6])
        if type == "Student":
            role_dropdown['values'] = get_filtered_role_names(institution_name) if get_filtered_role_names(institution_name) else ("No Roles Available")
            role_dropdown.set(role_name)
        else:
            role_dropdown['values'] = ("Volunteer")
            role_dropdown.set("Volunteer")
        role_dropdown.grid(row=2, column=4, pady=10, sticky='w')

        attending_days_label = tk.Label(edit_volunteer_popup, text="Attending Days", font=('Arial', 15), bg="white", fg="black")
        attending_days_label.grid(row=3, column=3, pady=10)
        attending_days_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black")
        attending_days_entry.insert(0, str(volunteer_details[8]))
        attending_days_entry.grid(row=3, column=4, pady=10, sticky='w')

        contract_length_label = tk.Label(edit_volunteer_popup, text="Contract Length", font=('Arial', 15), bg="white", fg="black")
        contract_length_label.grid(row=4, column=3, pady=10)
        contract_length = tk.StringVar(edit_volunteer_popup)
        contract_length_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black", textvariable=contract_length)
        contract_length_entry.insert(0, str(volunteer_details[9]))
        contract_length_entry.grid(row=4, column=4, pady=10, sticky='w')

        status_dropdown_label = tk.Label(edit_volunteer_popup, text="Status", font=('Arial', 15), bg="white", fg="black")
        status_dropdown_label.grid(row=5, column=3, pady=10)
        status_var = tk.StringVar(edit_volunteer_popup)
        status_dropdown = ttk.Combobox(edit_volunteer_popup, width=34, textvariable=status_var)
        status_dropdown['values'] = ("Signing Forms", "Ready to Start", "Awaiting Badge", "Badged")
        status_dropdown.insert(0, str(volunteer_details[10]))
        status_dropdown.grid(row=5, column=4, pady=10, sticky='w')
        status = status_dropdown.get()

        badge_number_label = tk.Label(edit_volunteer_popup, text="Badge Number", font=('Arial', 15), bg="white", fg="black")
        badge_number_label.grid(row=6, column=3, pady=10)
        badge_number_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black", state='normal' if status in ['Awaiting Badge', 'Badged'] else 'disabled')
        badge_number_entry.insert(0, str(volunteer_details[11]))
        badge_number_entry.grid(row=6, column=4, pady=10, sticky='w')

        project_label = tk.Label(edit_volunteer_popup, text="Project", font=('Arial', 15), bg="white", fg="black")
        project_label.grid(row=7, column=3, pady=10)
        project_entry = tk.Entry(edit_volunteer_popup, font=('Arial', 15), bg="white", fg="black", state='normal' if status in ['Awaiting Badge', 'Badged'] else 'disabled')
        project_entry.insert(0, str(volunteer_details[12]))
        project_entry.grid(row=7, column=4, pady=10, sticky='w')

        type_dropdown.bind("<<ComboboxSelected>>", lambda selected: on_type_select(selected, False, type_dropdown, institution_dropdown, role_dropdown, contract_length) if type_dropdown.get() == "Student" else on_type_select(selected, True, type_dropdown, institution_dropdown, role_dropdown, contract_length))

        institution_dropdown.bind("<<ComboboxSelected>>", lambda selected: on_institution_select(selected, False, institution_dropdown, role_dropdown) if type_dropdown.get() == "Student" else on_institution_select(selected, True, institution_dropdown, role_dropdown))

        status_dropdown.bind("<<ComboboxSelected>>", lambda selected: on_status_select(selected, status_dropdown, badge_number_entry, project_entry))

        edit_volunteer_button = ttk.Button(edit_volunteer_popup, text="Save", style="Blue.TButton", command=lambda: on_volunteer_submit(volunteer_details[0], name_entry.get(), email_entry.get(), phone_entry.get(), type_dropdown, institution_dropdown, role_dropdown, start_date_chooser.get_date(), attending_days_entry.get(), contract_length_entry.get(), status_dropdown, badge_number_entry.get(), project_entry.get(), 'Edit', edit_volunteer_popup))
        edit_volunteer_button.grid(row=8, column=0, pady=10, columnspan=5)

    header = tk.Label(edit_volunteer_popup, text= "Edit Volunteer", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=270, pady=10, columnspan=5)

    volunteer_dropdown_label = tk.Label(edit_volunteer_popup, text="Volunteer", font=('Arial', 15), bg="white", fg="black")
    volunteer_dropdown_label.grid(row=1, column=1, pady=10)
    volunteer_var = tk.StringVar(edit_volunteer_popup)
    volunteer_dropdown = ttk.Combobox(edit_volunteer_popup, width=34, textvariable=volunteer_var, state='readonly')
    volunteer_dropdown['values'] = get_volunteer_names() if get_volunteer_names() else ("No Volunteers Available")
    volunteer_dropdown.grid(row=1, column=2, sticky='w', pady=10, columnspan=5)
    volunteer_dropdown.bind("<<ComboboxSelected>>", edit_volunteer_popup_specific)
    

def edit_institution_popup():
    edit_institution_popup = tk.Toplevel(root)
    edit_institution_popup.title("Edit Institution")
    edit_institution_popup.geometry("470x350")
    edit_institution_popup.configure(bg="white")
    edit_institution_popup.resizable(False, False)

    def edit_institution_popup_specific(selected):

        institution_details = get_institution(institution_dropdown.get())
        name_label = tk.Label(edit_institution_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
        name_label.grid(row=2, column=0, pady=10)
        name_entry = tk.Entry(edit_institution_popup, font=('Arial', 15), bg="white", fg="black")
        name_entry.insert(0, str(institution_details[1]))
        name_entry.grid(row=2, column=1, pady=10, sticky='w')

        type_label = tk.Label(edit_institution_popup, text="Type", font=('Arial', 15), bg="white", fg="black")
        type_label.grid(row=3, column=0, pady=10)
        type_var = tk.StringVar(edit_institution_popup)
        type_dropdown = ttk.Combobox(edit_institution_popup, width=34, textvariable=type_var)
        type_dropdown['values'] = ('University', 'College')
        if institution_details[2] in type_dropdown['values']:
            type_dropdown.set(institution_details[2].strip())
        type_dropdown.grid(row=3, column=1, pady=10, sticky='w')
        edit_institution_popup.update_idletasks()

        postcode_label = tk.Label(edit_institution_popup, text="Postcode", font=('Arial', 15), bg="white", fg="black")
        postcode_label.grid(row=4, column=0, pady=10)
        postcode_entry = tk.Entry(edit_institution_popup, font=('Arial', 15), bg="white", fg="black")
        postcode_entry.insert(0, str(institution_details[3]))
        postcode_entry.grid(row=4, column=1, pady=10, sticky='w')

        edit_institution_button = ttk.Button(edit_institution_popup, text="Save", style="Blue.TButton", command=lambda: on_institution_submit(institution_details[0], name_entry.get(), type_dropdown, postcode_entry.get(), 'Edit', edit_institution_popup))
        edit_institution_button.grid(row=5, column=0, pady=10, columnspan=2)

    header = tk.Label(edit_institution_popup, text= "Edit Institution", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    institution_dropdown_label = tk.Label(edit_institution_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
    institution_dropdown_label.grid(row=1, column=0, pady=10)
    institution_var = tk.StringVar(edit_institution_popup)
    institution_dropdown = ttk.Combobox(edit_institution_popup, width=34, textvariable=institution_var, state='readonly')
    institution_dropdown['values'] = get_institution_names() if get_institution_names() else ("No Institutions Available")
    institution_dropdown.grid(row=1, column=1, sticky='w', pady=10)
    institution_dropdown.bind("<<ComboboxSelected>>", edit_institution_popup_specific)

def edit_role_popup():
    edit_role_popup = tk.Toplevel(root)
    edit_role_popup.title("Edit Role")
    edit_role_popup.geometry("470x420")
    edit_role_popup.configure(bg="white")
    edit_role_popup.resizable(False, False)

    def edit_role_popup_specific(selected):

        role_details, institution_names = get_role(role_dropdown.get())
        name_label = tk.Label(edit_role_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
        name_label.grid(row=2, column=0, pady=10)
        name_entry = tk.Entry(edit_role_popup, font=('Arial', 15), bg="white", fg="black")
        name_entry.insert(0, str(role_details[1]))
        name_entry.grid(row=2, column=1, sticky='w', pady=10)

        description_label = tk.Label(edit_role_popup, text="Description", font=('Arial', 15), bg="white", fg="black")
        description_label.grid(row=3, column=0, pady=10)
        description_entry = tk.Entry(edit_role_popup, font=('Arial', 15), bg="white", fg="black")
        description_entry.insert(0, str(role_details[2]))
        description_entry.grid(row=3, column=1, sticky='w', pady=10)

        institution_var = tk.StringVar(edit_role_popup)
        values = get_institution_names() if get_institution_names() else ("No Institutions Available")
        institutions_label = tk.Label(edit_role_popup, text="Select Institutions:", font=('Arial', 12), bg="white", fg="black")
        institutions_label.grid(row=4, column=0, pady=10, sticky='n')
        institutions = tk.Listbox(edit_role_popup, listvariable=institution_var, height=5, width=27, selectmode="multiple", bg="white", fg="black", font=('Arial', 12), exportselection=0, selectforeground="white", selectbackground="dark blue")
        for value in values:
            institutions.insert(tk.END, value)
        institutions.grid(row=4, column=1, sticky='w', pady=10)

        for name in institution_names:
            name = str(name).strip("[]\''")
            index = list(institutions.get(0, "end")).index(f'{name}')
            institutions.select_set(index)

        edit_role_button = ttk.Button(edit_role_popup, text="Save", style="Blue.TButton", command=lambda: on_role_submit(role_details[0], name_entry.get(), description_entry.get(), institutions, "Edit", edit_role_popup))
        edit_role_button.grid(row=6, column=0, pady=10, columnspan=2)

    header = tk.Label(edit_role_popup, text= "Edit Role", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)

    role_dropdown_label = tk.Label(edit_role_popup, text="Role", font=('Arial', 15), bg="white", fg="black")
    role_dropdown_label.grid(row=1, column=0, pady=10)
    role_var = tk.StringVar(edit_role_popup)
    role_dropdown = ttk.Combobox(edit_role_popup, width=34, textvariable=role_var, state='readonly')
    role_dropdown['values'] = get_role_names() if get_role_names() else ("No Roles Available")
    role_dropdown.grid(row=1, column=1, sticky='w', pady=10)
    role_dropdown.bind("<<ComboboxSelected>>", edit_role_popup_specific)

def edit_artist_popup():
    edit_artist_popup = tk.Toplevel(root)
    edit_artist_popup.title("Edit Artist")
    edit_artist_popup.geometry("470x350")
    edit_artist_popup.configure(bg="white")
    edit_artist_popup.resizable(False, False)

    def edit_artist_popup_specific(selected):

        artist_details = get_artist(artist_dropdown.get())
        name_label = tk.Label(edit_artist_popup, text="Name", font=('Arial', 15), bg="white", fg="black")
        name_label.grid(row=2, column=0, pady=10)
        name_entry = tk.Entry(edit_artist_popup, font=('Arial', 15), bg="white", fg="black")
        name_entry.insert(0, str(artist_details[1]))
        name_entry.grid(row=2, column=1, sticky='w', pady=10)

        email_label = tk.Label(edit_artist_popup, text="E-Mail", font=('Arial', 15), bg="white", fg="black")
        email_label.grid(row=3, column=0, pady=10)
        email_entry = tk.Entry(edit_artist_popup, font=('Arial', 15), bg="white", fg="black")
        email_entry.insert(0, str(artist_details[2]))
        email_entry.grid(row=3, column=1, sticky='w', pady=10)

        phone_label = tk.Label(edit_artist_popup, text="Phone", font=('Arial', 15), bg="white", fg="black")
        phone_label.grid(row=4, column=0, pady=10)
        phone_entry = tk.Entry(edit_artist_popup, font=('Arial', 15), bg="white", fg="black")
        phone_entry.insert(0, str(artist_details[3]))
        phone_entry.grid(row=4, column=1, sticky='w', pady=10)

        edit_artist_button = ttk.Button(edit_artist_popup, text="Save", style="Blue.TButton", command=lambda: on_artist_submit(artist_details[0], name_entry.get(), email_entry.get(), phone_entry.get(), "Edit", edit_artist_popup))
        edit_artist_button.grid(row=5, column=0, pady=10, columnspan=2)

    header = tk.Label(edit_artist_popup, text= "Edit Artist", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=140, pady=10, columnspan=2)
    
    artist_dropdown_label = tk.Label(edit_artist_popup, text="Artist", font=('Arial', 15), bg="white", fg="black")
    artist_dropdown_label.grid(row=1, column=0, pady=10)
    artist_var = tk.StringVar(edit_artist_popup)
    artist_dropdown = ttk.Combobox(edit_artist_popup, width=34, textvariable=artist_var, state='readonly')
    artist_dropdown['values'] = get_artist_names() if get_artist_names() else ("No Artists Available")
    artist_dropdown.grid(row=1, column=1, sticky='w', pady=10)
    artist_dropdown.bind("<<ComboboxSelected>>", edit_artist_popup_specific)

'''Deleting Popups'''

def delete_volunteer_popup():
    delete_volunteer_popup = tk.Toplevel(root)
    delete_volunteer_popup.title("Delete Volunteer")
    delete_volunteer_popup.geometry("470x200")
    delete_volunteer_popup.configure(bg="white")
    delete_volunteer_popup.resizable(False, False)

    header = tk.Label(delete_volunteer_popup, text= "Delete Volunteer", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=90, pady=10, columnspan=2)

    volunteer_names = get_volunteer_names()

    if volunteer_names:
        volunteer_dropdown_label = tk.Label(delete_volunteer_popup, text="Volunteer", font=('Arial', 15), bg="white", fg="black")
        volunteer_dropdown_label.grid(row=1, column=0, pady=10)
        volunteer_var = tk.StringVar(delete_volunteer_popup)
        volunteer_dropdown = ttk.Combobox(delete_volunteer_popup, width=34, textvariable=volunteer_var)
        volunteer_dropdown['values'] = volunteer_names
        volunteer_dropdown.grid(row=1, column=1, sticky='w', pady=10)

        delete_volunteer_button = ttk.Button(delete_volunteer_popup, text="Delete", style="Blue.TButton", command=lambda: [delete_volunteer(volunteer_dropdown.get()), delete_volunteer_popup.destroy()])
        delete_volunteer_button.grid(row=2, column=0, pady=10, columnspan=2)
    else:
        no_volunteers_label = tk.Label(delete_volunteer_popup, text="No volunteers to delete", font=('Arial', 15), bg="white", fg="black")
        no_volunteers_label.grid(row=1, column=0, pady=10, columnspan=2)

def delete_institution_popup():
    delete_institution_popup = tk.Toplevel(root)
    delete_institution_popup.title("Delete Institution")
    delete_institution_popup.geometry("470x250")
    delete_institution_popup.configure(bg="white")
    delete_institution_popup.resizable(False, False)

    def delete_institution_popup_specific(selected):
        nonlocal delete_institution_frame
        delete_institution_frame.destroy()
        delete_institution_frame = tk.Frame(delete_institution_popup, bg='white')
        delete_institution_frame.grid(row=2, column=0, pady=10, columnspan=2)

        if delete_institution_eligibility(institution_dropdown.get()):
            delete_institution_button = ttk.Button(delete_institution_frame, text="Delete", style="Blue.TButton", command=lambda: [delete_institution(institution_dropdown.get()), delete_institution_popup.destroy()])
            delete_institution_button.grid(row=0, column=0, pady=10, columnspan=2)
        else:
            warning_label = tk.Label(delete_institution_frame, text='Volunteers in the system are linked to this institution, unable to delete', font=('Arial', 10), bg="white", fg="red" )
            warning_label.grid(row=0, column=0, pady=10, columnspan=2)
            delete_institution_button = ttk.Button(delete_institution_frame, text="Delete", style="Blue.TButton", state='disabled')
            delete_institution_button.grid(row=1, column=0, pady=10, columnspan=2)

    header = tk.Label(delete_institution_popup, text= "Delete Institution", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=90, pady=10, columnspan=2)

    institution_names = get_institution_names()

    if institution_names:
        institution_dropdown_label = tk.Label(delete_institution_popup, text="Institution", font=('Arial', 15), bg="white", fg="black")
        institution_dropdown_label.grid(row=1, column=0, pady=10)
        institution_var = tk.StringVar(delete_institution_popup)
        institution_dropdown = ttk.Combobox(delete_institution_popup, width=34, textvariable=institution_var, state='readonly')
        institution_dropdown['values'] = institution_names
        institution_dropdown.grid(row=1, column=1, sticky='w', pady=10)
        institution_dropdown.bind("<<ComboboxSelected>>", delete_institution_popup_specific)
    else:
        no_institutions_label = tk.Label(delete_institution_popup, text="No institutions to delete", font=('Arial', 15), bg="white", fg="black")
        no_institutions_label.grid(row=1, column=0, pady=10, columnspan=2)

    delete_institution_frame = tk.Frame(delete_institution_popup, bg='white')
    delete_institution_frame.grid(row=2, column=0, pady=10, columnspan=2)

def delete_role_popup():
    delete_role_popup = tk.Toplevel(root)
    delete_role_popup.title("Delete Role")
    delete_role_popup.geometry("470x250")
    delete_role_popup.configure(bg="white")
    delete_role_popup.resizable(False, False)

    def delete_role_popup_specific(selected):
        nonlocal delete_role_frame
        delete_role_frame.destroy()
        delete_role_frame = tk.Frame(delete_role_popup, bg='white')
        delete_role_frame.grid(row=2, column=0, columnspan=2)

        if delete_role_eligibility(role_dropdown.get()):
            delete_role_button = ttk.Button(delete_role_frame, text="Delete", style="Blue.TButton", command=lambda: [delete_role(role_dropdown.get()), delete_role_popup.destroy()])
            delete_role_button.grid(row=0, column=0, pady=10, columnspan=2)
        else:
            warning_label = tk.Label(delete_role_frame, text='Volunteers in the system are linked to this role, unable to delete', font=('Arial', 10), bg="white", fg="red" )
            warning_label.grid(row=0, column=0, pady=10, columnspan=2)
            delete_role_button = ttk.Button(delete_role_frame, text="Delete", style="Blue.TButton", state='disabled')
            delete_role_button.grid(row=1, column=0, pady=10, columnspan=2)

    header = tk.Label(delete_role_popup, text= "Delete Role", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=130, pady=10, columnspan=2)

    role_names = get_role_names()

    if role_names:
        role_dropdown_label = tk.Label(delete_role_popup, text="Role", font=('Arial', 15), bg="white", fg="black")
        role_dropdown_label.grid(row=1, column=0, pady=10)
        role_var = tk.StringVar(delete_role_popup)
        role_dropdown = ttk.Combobox(delete_role_popup, width=34, textvariable=role_var, state='readonly')
        role_dropdown['values'] = role_names
        role_dropdown.grid(row=1, column=1, sticky='w', pady=10)
        role_dropdown.bind("<<ComboboxSelected>>", delete_role_popup_specific)
    else:
        no_roles_label = tk.Label(delete_role_popup, text="No roles to delete", font=('Arial', 15), bg="white", fg="black")
        no_roles_label.grid(row=1, column=0, pady=10, columnspan=2)

    delete_role_frame = tk.Frame(delete_role_popup, bg='white')
    delete_role_frame.grid(row=2, column=0, columnspan=2)

def delete_artist_popup():
    delete_artist_popup = tk.Toplevel(root)
    delete_artist_popup.title("Delete Artist")
    delete_artist_popup.geometry("470x200")
    delete_artist_popup.configure(bg="white")
    delete_artist_popup.resizable(False, False)

    header = tk.Label(delete_artist_popup, text= "Delete Artist", font=('Arial', 30), bg="white", fg="dark blue")
    header.grid(row=0, column=0, padx=110, pady=10, columnspan=2)

    artist_names = get_artist_names()

    if artist_names:
        artist_dropdown_label = tk.Label(delete_artist_popup, text="Artist", font=('Arial', 15), bg="white", fg="black")
        artist_dropdown_label.grid(row=1, column=0, pady=10)
        artist_var = tk.StringVar(delete_artist_popup)
        artist_dropdown = ttk.Combobox(delete_artist_popup, width=34, textvariable=artist_var, state='readonly')
        artist_dropdown['values'] = artist_names
        artist_dropdown.grid(row=1, column=1, sticky='w', pady=10)

        delete_role_button = ttk.Button(delete_artist_popup, text="Delete", style="Blue.TButton", command=lambda: [delete_artist(artist_dropdown.get()), delete_artist_popup.destroy()])
        delete_role_button.grid(row=2, column=0, pady=10, columnspan=2)
    else:
        no_artists_label = tk.Label(delete_artist_popup, text="No artists to delete", font=('Arial', 15), bg="white", fg="black")
        no_artists_label.grid(row=1, column=0, pady=10, columnspan=2)


'''Main Menu'''

header = tk.Label(root, text="Welcome", font=("Arial", 60), bg="white", fg="dark blue")
header.grid(row=0, column=0, columnspan=2, sticky="nsw", padx=120, pady=35)

view_button = ttk.Button(root, text="View", style="Blue.TButton", command=lambda: [view_options_popup(), root.iconify()])
view_button.grid(row=1, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

add_button = ttk.Button(root, text="Add", style="Blue.TButton", command=lambda: [add_options_popup(), root.iconify()])
add_button.grid(row=1, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

edit_button = ttk.Button(root, text="Edit", style="Blue.TButton", command=lambda: [edit_options_popup(), root.iconify()])
edit_button.grid(row=2, column=0, ipadx=30, ipady=20, padx=10, pady=10, sticky="nse")

delete_button = ttk.Button(root, text="Delete", style="Blue.TButton", command=lambda: [delete_options_popup(), root.iconify()])
delete_button.grid(row=2, column=1, ipadx=30, ipady=20, padx=10, pady=10, sticky="nsw")

root.mainloop()

