import sqlite3

# Établir une connexion à la base de données
def get_conn(database_name):
    return sqlite3.connect(database_name)

conn = sqlite3.connect('users.db')

# Créer les tables
conn.execute('DROP TABLE IF EXISTS comptes;')
conn.execute('DROP TABLE IF EXISTS patients;')

def create_movies_table(conn):
    conn.execute('''CREATE TABLE movies (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    id               TEXT NOT NULL,
                    username         TEXT,
                    full_name        TEXT,
                    email            TEXT,
                    hashed_password  TEXT
                  );''')

def create_patients_table(conn):
    conn.execute('''CREATE TABLE patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom VARCHAR(50),
                    prenom VARCHAR(50),
                  );''')

def insert_data_into_comptes_table(conn):
    conn.execute('''INSERT INTO comptes (id, username, full_name, email, hashed_password)
                    VALUES ('1', 'johndoe', 'John Doe', 'johndoe@example.com', 'pwd_context.hash("bonjour")'),
                           ('2', 'alicefontaine', 'Alice Fontaine', 'alicefontaine@example.com', 'pwd_context.hash("salut")');''')

def insert_data_into_patients_table(conn):
    conn.execute('''INSERT INTO patients (nom, prenom)
                    VALUES ('Doe', 'John'),
                           ('Fontaine', 'Alice');''')

def close_connection(conn):
    conn.close()

