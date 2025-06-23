BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "artists" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"email"	TEXT NOT NULL UNIQUE,
	"phone"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "institution_roles" (
	"institution_id"	INTEGER,
	"role_id"	INTEGER,
	PRIMARY KEY("institution_id","role_id"),
	FOREIGN KEY("institution_id") REFERENCES "institutions"("id") ON DELETE CASCADE,
	FOREIGN KEY("role_id") REFERENCES "roles"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "institutions" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"type"	TEXT NOT NULL,
	"postcode"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "roles" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL UNIQUE,
	"description"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "volunteers" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"phone"	TEXT,
	"type"	TEXT,
	"institution_id"	TEXT,
	"role_id"	TEXT,
	"start_date"	TEXT,
	"attending_days"	TEXT,
	"contract_length"	TEXT,
	"status"	TEXT,
	"badge_number"	TEXT,
	"project"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("institution_id") REFERENCES "institutions"("id"),
	FOREIGN KEY("role_id") REFERENCES "roles"("id")
);
COMMIT;
