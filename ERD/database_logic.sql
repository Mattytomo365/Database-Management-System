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
    badge_number TEXT,
    project TEXT,
    FOREIGN KEY (institution_id) REFERENCES institutions(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
)

    CREATE TABLE IF NOT EXISTS institutions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    type TEXT NOT NULL,
    postcode TEXT
)

    CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT
)

    CREATE TABLE IF NOT EXISTS institution_roles (
    institution_id INTEGER,
    role_id INTEGER,
    PRIMARY KEY (institution_id, role_id),
    FOREIGN KEY (institution_id) REFERENCES institutions(id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
)

    CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    phone TEXT
)