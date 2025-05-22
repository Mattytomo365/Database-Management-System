import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor() # A mechanism that enables traversal of records in a database

# Create tables

def create_volunteer_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            type TEXT,
            institution TEXT,
            role TEXT,
            start_date TEXT,
            contract_length TEXT,
            status TEXT
        )
    ''')
    connection.commit()

def create_institution_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            location TEXT
        )
    ''')
    connection.commit()

def create_role_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    connection.commit()

def create_artist_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT
        )
    ''')
    connection.commit()

# Add functions

def add_volunteer():
    pass

def add_institution():
    pass

def add_artist():
    pass

# Edit functions

def edit_volunteer():
    pass

def edit_institution():
    pass

def edit_artist():
    pass

# Delete functions

def delete_volunteer():
    pass

def delete_institution():
    pass

def delete_artist():
    pass

# View functions

def retrieve_students():
    pass

def retrieve_volunteers():
    pass

def retrieve_universities():
    pass

def retrieve_colleges():
    pass

def retrieve_roles(institution_name):
    pass

def retrieve_artists():
    pass


