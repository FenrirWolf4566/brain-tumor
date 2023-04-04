import sqlite3

# Établir une connexion à la base de données
conn = sqlite3.connect('matable.db')

# Créer les tables
conn.execute('DROP TABLE IF EXISTS comptes;')
conn.execute('DROP TABLE IF EXISTS patients;')
conn.execute('''CREATE TABLE movies (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                id               TEXT NOT NULL,
                username         TEXT,
                full_name        TEXT,
                email            TEXT,
                hashed_password  TEXT
              );''')
conn.execute('''CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(50),
                prenom VARCHAR(50),
              );''')

# Insérer les données
conn.execute('''INSERT INTO comptes (id, username, full_name, email, hashed_password)
                VALUES ('1', 'johndoe', 'John Doe', 'johndoe@example.com', 'pwd_context.hash("bonjour")'),
                       ('2', 'alicefontaine', Alice Fontaine, 'alicefontaine@example.com', 'pwd_context.hash("salut")');''')

conn.execute('''INSERT INTO patients (nom, prenom)
                VALUES ('Doe', 'John'),
                       ('Fontaine', 'Alice');''')

# Fermer la connexion
conn.close()
