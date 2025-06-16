import sqlite3

connection = sqlite3.connect('database.db')
connection.execute("PRAGMA foreign_keys = ON")
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
            PRIMARY KEY (institution_id, role_id),
            FOREIGN KEY (institution_id) REFERENCES institutions(id) ON DELETE CASCADE,
            FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
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

def add_volunteer(name, email, phone, type, institution_name, role_name, start_date, attending_days, contract_length, status):

    if institution_name == ' ':
        institution_id = None
        
    else:
        institution_id = get_id('institutions', institution_name)

    role_id = get_id('roles', role_name)
    
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

        institution_id = get_id('institutions', institution_name)

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

def edit_volunteer(volunteer_id, name, email, phone, type, institution_name, role_name, start_date, attending_days, contract_length, status):

    institution_id = get_id('institutions', institution_name)

    role_id = get_id('roles', role_name)

    cursor.execute('''
        UPDATE volunteers
        SET name = ?, email = ?, phone = ?, type = ?, institution_id = ?, role_id = ?, start_date = ?, attending_days = ?, contract_length = ?, status = ?
        WHERE id = ?''', (name, email, phone, type, institution_id, role_id, start_date, attending_days, contract_length, status, volunteer_id))
    connection.commit()


def edit_institution(institution_id, name, type, postcode):
    cursor.execute('''
        UPDATE institutions
        SET name = ?, type = ?, postcode = ?
        WHERE id = ?''', (name, type, postcode, institution_id))
    connection.commit()


def edit_role(role_id, name, description, institution_names):

    institution_names = institution_names.split(', ')

    cursor.execute('''
        UPDATE roles
        SET name = ?, description = ?
        WHERE id = ?''', (name, description, role_id))
    connection.commit()

    institution_ids = []
    for institution_name in institution_names:
        institution_id = get_id('institutions', institution_name)
        
        if institution_id:
            institution_ids.append(institution_id)

        else:
            institution_ids.append('Institution ID not found')

    cursor.execute('SELECT institution_id FROM institution_roles WHERE role_id = ?', (role_id,))
    connection.commit()
    original_institution_ids = [int(row[0]) for row in cursor.fetchall()]

    deletable_institution_ids = []
    for original_institution_id in original_institution_ids:

        for institution_id in institution_ids:

            if original_institution_id == institution_id:
                delete = False
                break
            else:
                delete = True

        if delete:
            deletable_institution_ids.append(original_institution_id)

    for institution_id in institution_ids:
            cursor.execute('''
                INSERT OR IGNORE INTO institution_roles (institution_id, role_id)
                VALUES (?, ?)''', (institution_id, role_id))
            connection.commit()

    for deletable_id in deletable_institution_ids:
        cursor.execute('DELETE FROM institution_roles WHERE institution_id = ? AND role_id = ?', (deletable_id, role_id))
    connection.commit()


def edit_artist(artist_id, name, email, phone):
    cursor.execute('''
        UPDATE artists
        SET name = ?, email = ?, phone = ?
        WHERE id = ?''', (name, email, phone, artist_id))
    connection.commit()

# Delete functions

def delete_volunteer(name):
    volunteer_id = get_id('volunteers', name)

    cursor.execute('DELETE FROM volunteers WHERE id = ?', (volunteer_id,))
    connection.commit()


def delete_institution_eligibility(institution_name):

    institution_id = get_id('institutions', institution_name)

    cursor.execute('SELECT institution_id FROM volunteers')
    connection.commit()
    volunteer_institution_ids = [int(row[0]) for row in cursor.fetchall()]

    for volunteer_institution_id in volunteer_institution_ids:
        if volunteer_institution_id == institution_id:
            return False
    return True


def delete_institution(name):
    connection.execute("PRAGMA foreign_keys = ON")

    institution_id = ('institutions', name)

    cursor.execute('DELETE FROM institutions WHERE id = ?', (institution_id,))
    connection.commit()


def delete_role_eligibility(name):
    role_id = get_id('roles', name)

    cursor.execute('SELECT role_id FROM volunteers')
    connection.commit()
    volunteer_role_ids = [int(row[0]) for row in cursor.fetchall()]

    for volunteer_role_id in volunteer_role_ids:
        if volunteer_role_id == role_id:
            return False
    return True


def delete_role(name):
    connection.execute("PRAGMA foreign_keys = ON")

    role_id = get_id('roles', name)

    cursor.execute('DELETE FROM roles WHERE id = ?', (role_id,))
    connection.commit()


def delete_artist(name):
    artist_id = get_id('artists', name)

    connection.execute('DELETE FROM artists WHERE id = ?', (artist_id,))
    connection.commit()

# Retrieval functions

def get_id(table_name, record_name):
    cursor.execute(f'SELECT id from {table_name} WHERE name = ?', (record_name,))
    connection.commit()
    id = cursor.fetchone()[0]
    return id if id else None


def get_volunteer_names():
    cursor.execute('SELECT name FROM volunteers')
    connection.commit()
    return [row[0] for row in cursor.fetchall()]

def get_volunteers():
    cursor.execute('SELECT * FROM volunteers')
    connection.commit()
    return cursor.fetchall()

def get_volunteer(name):
    cursor.execute('SELECT * FROM volunteers WHERE name = ?', (name,))
    connection.commit()
    return cursor.fetchone()

def get_filtered_volunteers(type):
    cursor.execute('SELECT * FROM volunteers WHERE type = ?', (type,))
    connection.commit()
    return cursor.fetchall()

def get_institution_names():
    cursor.execute('SELECT name FROM institutions')
    connection.commit()
    return [row[0] for row in cursor.fetchall()]

def get_institution_name(id):
    if id == None:
        return "N/A"
    else:
        cursor.execute('SELECT name FROM institutions WHERE id = ?', (id,))
    connection.commit()
    return cursor.fetchone()[0]

def get_institutions():
    cursor.execute('SELECT * FROM institutions')
    connection.commit()
    return cursor.fetchall()

def get_institution(name):
    cursor.execute('SELECT * FROM institutions WHERE name = ?', (name,))
    connection.commit()
    return cursor.fetchone()

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

def get_role(name):
    cursor.execute('SELECT * FROM roles WHERE name = ?', (name,))
    connection.commit()
    role_details = cursor.fetchone()

    cursor.execute('SELECT institution_id FROM institution_roles WHERE role_id = ?', (role_details[0],))
    institution_ids = [int(row[0]) for row in cursor.fetchall()]

    institutions = []

    for institution_id in institution_ids:
        cursor.execute('SELECT name FROM institutions WHERE id = ?', (institution_id,))
        connection.commit()
        institution = [row[0] for row in cursor.fetchall()]

        if institution:
            institutions.append(institution)
        else:
            institutions.append('No institutions offer this role')

    return role_details, institutions

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

def get_filtered_role_names(institution):
    cursor.execute('SELECT id FROM institutions WHERE name = ?', (institution,))
    connection.commit()
    institution_id = cursor.fetchone()[0]

    cursor.execute('SELECT role_id FROM institution_roles WHERE institution_id = ?', (institution_id,))
    connection.commit()
    role_ids = [int(row[0]) for row in cursor.fetchall()]

    role_names = []

    for role_id in role_ids:
        cursor.execute('SELECT name FROM roles WHERE id = ?', (role_id,))
        role_name = cursor.fetchone()[0]
        if role_name:
            role_names.append(role_name)

    return role_names

def get_artist_names():
    cursor.execute('SELECT name FROM artists')
    connection.commit()
    artist_names = [row[0] for row in cursor.fetchall()]
    return artist_names

def get_artists():
    cursor.execute('SELECT * FROM artists')
    connection.commit()
    return cursor.fetchall()

def get_artist(name):
    cursor.execute('SELECT * FROM artists WHERE name = ?', (name,))
    connection.commit()
    return cursor.fetchone()

# Initialisation of database function

def initialise_database():
    create_volunteer_table()
    create_institution_table()
    create_role_table()
    create_institution_role_table()
    create_artist_table()


