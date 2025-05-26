import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor() # A mechanism that enables traversal of records in a database

# Create tables

def create_volunteer_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            type TEXT NOT NULL,
            postcode TEXT
        )
    ''')
    connection.commit()

def create_role_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS roles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    connection.commit()

def create_artist_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS artists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            phone TEXT
        )
    ''')
    connection.commit()

# Add functions

def add_volunteer():
    pass

def add_institution(name, type, postcode):
    cursor.execute('''
        INSERT INTO institutions (name, type, postcode)
        VALUES (?, ?, ?)'''
        , (name, type, postcode))
    connection.commit()

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

# Other functions

def get_institution_names():
    cursor.execute('SELECT name FROM institutions')
    connection.commit()
    institution_names = [row[0] for row in cursor.fetchall()]
    return institution_names

def get_role_names():
    cursor.execute('SELECT name FROM roles')
    connection.commit()
    return cursor.fetchall()

def initialise_database():
    create_volunteer_table()
    create_institution_table()
    create_role_table()
    create_artist_table()


