import sqlite3

# Établir une connexion à la base de données
def get_conn(database_name):
    return sqlite3.connect(database_name)

conn = sqlite3.connect('users.db')

# Créer les tables
conn.execute('DROP TABLE IF EXISTS comptes;')
conn.execute('DROP TABLE IF EXISTS patients;')

def create_comptes_table(conn):
    conn.execute('''CREATE TABLE comptes (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    id               TEXT NOT NULL,
                    username         TEXT,
                    full_name        TEXT,
                    email            TEXT,
                    hashed_password  TEXT
                  );''')

def insert_data_into_patients_table(conn):
    conn.execute('''INSERT INTO patients (nom, prenom)
                    VALUES ('Doe', 'John'),
                           ('Fontaine', 'Alice');''')

def close_connection(conn):
    conn.close()

