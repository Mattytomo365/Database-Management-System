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
            institution_id TEXT,
            role_id TEXT,
            start_date TEXT,
            attending_days TEXT,
            contract_length TEXT,
            status TEXT,
            FOREIGN KEY (institution_id) REFERENCES institutions(id),
            FOREIGN KEY (role_id) REFERENCES roles(id)
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

def create_institution_role_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS institution_roles (
            institution_id INTEGER,
            role_id INTEGER,
            FOREIGN KEY (institution_id) REFERENCES institutions(id),
            FOREIGN KEY (role_id) REFERENCES roles(id),
            PRIMARY KEY (institution_id, role_id)
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

def add_volunteer(name, email, phone, type, institution, role, start_date, attending_days, contract_length, status):
    cursor.execute('''
        SELECT id FROM institutions WHERE name = ?
        ''', (institution,))
    
    institution_id = cursor.fetchone()[0]

    cursor.execute('''
        SELECT id FROM roles WHERE name = ?
        ''', (role,))
    
    role_id = cursor.fetchone()[0]
    
    cursor.execute('''
        INSERT INTO volunteers (name, email, phone, type, institution_id, role_id, start_date, attending_days, contract_length, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        , (name, email, phone, type, institution_id, role_id, start_date, attending_days, contract_length, status))
    connection.commit()


def add_institution(name, type, postcode):
    cursor.execute('''
        INSERT INTO institutions (name, type, postcode)
        VALUES (?, ?, ?)'''
        , (name, type, postcode))
    connection.commit()


def add_role(name, description, institution_names):
    
    institution_names = institution_names.split(', ')

    cursor.execute('''
        INSERT INTO roles (name, description)
        VALUES (?, ?)
        ''', (name, description))
    connection.commit()
    
    role_id = cursor.lastrowid
    
    for institution_name in institution_names:
        cursor.execute('''
            SELECT id FROM institutions WHERE name = ?
        ''', (institution_name,))
    
        institution_id = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO institution_roles (role_id, institution_id)
            VALUES (?, ?)
        ''', (role_id, institution_id))
        connection.commit()


def add_artist(name, email, phone):
    cursor.execute('''
        INSERT INTO artists (name, email, phone)
        VALUES (?, ?, ?)
    ''', (name, email, phone))
    connection.commit()

# Edit functions

def edit_volunteer():
    pass

def edit_institution():
    pass

def edit_role():
    pass

def edit_artist():
    pass

# Delete functions

def delete_volunteer():
    pass

def delete_institution():
    pass

def delete_role():
    pass

def delete_artist():
    pass

# Retrieval functions

def get_volunteer_names():
    cursor.execute('SELECT name FROM volunteers')
    connection.commit()
    return [row[0] for row in cursor.fetchall()]

def get_volunteers():
    cursor.execute('SELECT * FROM volunteers')
    connection.commit()
    return cursor.fetchall()

def get_filtered_volunteers(type):
    cursor.execute('SELECT * FROM volunteers WHERE type = ?', (type,))
    connection.commit()
    return cursor.fetchall()

def get_institution_names():
    cursor.execute('SELECT name FROM institutions')
    connection.commit()
    return [row[0] for row in cursor.fetchall()]

def get_institution_name(id):
    cursor.execute('SELECT name FROM institutions WHERE id = ?', (id,))
    connection.commit()
    return cursor.fetchone()[0]

def get_institutions():
    cursor.execute('SELECT * FROM institutions')
    connection.commit()
    return cursor.fetchall()

def get_filtered_institutions(type):
    cursor.execute('SELECT * FROM institutions WHERE type = ?', (type,))
    connection.commit()
    return cursor.fetchall()

def get_role_names():
    cursor.execute('SELECT name FROM roles')
    connection.commit()
    return [row[0] for row in cursor.fetchall()]

def get_role_name(id):
    cursor.execute('SELECT name FROM roles WHERE id = ?', (id,))
    connection.commit()
    return cursor.fetchone()[0]

def get_roles():
    cursor.execute('SELECT * FROM roles')
    connection.commit()
    return cursor.fetchall()

def get_filtered_roles(institution):
    cursor.execute('SELECT id FROM institutions WHERE name = ?', (institution,))
    connection.commit()
    institution_id = cursor.fetchone()[0]

    cursor.execute('SELECT role_id FROM institution_roles WHERE institution_id = ?', (institution_id,))
    connection.commit()
    role_ids = [int(row[0]) for row in cursor.fetchall()]

    roles = []

    for role_id in role_ids:
        cursor.execute('SELECT * FROM roles WHERE id = ?', (role_id,))
        role = cursor.fetchone()
        if role:
            roles.append(role)

    return roles

def get_artist_names():
    cursor.execute('SELECT name FROM artists')
    connection.commit()
    artist_names = [row[0] for row in cursor.fetchall()]
    return artist_names

def get_artists():
    cursor.execute('SELECT * FROM artists')
    connection.commit()
    return cursor.fetchall()

# Initialisation of database function

def initialise_database():
    create_volunteer_table()
    create_institution_table()
    create_role_table()
    create_institution_role_table()
    create_artist_table()


