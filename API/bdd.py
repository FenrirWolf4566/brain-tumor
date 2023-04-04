import sqlite3

# Établir une connexion à la base de données
conn = sqlite3.connect('matable.db')

# Créer les tables
conn.execute('DROP TABLE IF EXISTS comptes;')
conn.execute('DROP TABLE IF EXISTS patients;')
conn.execute('''CREATE TABLE movies (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                title            TEXT NOT NULL,
                primary_director TEXT,
                year_released    INT,
                genre            TEXT
              );''')
conn.execute('''CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom VARCHAR(50),
                prenom VARCHAR(50),
                age INT
              );''')

# Insérer les données
conn.execute('''INSERT INTO comptes (id, username, full_name, hashed_password)
                VALUES ('1', 'johndoe', 1997, 'sci-fi'),
                       ('Pirates of the Caribbean: The Curse of the Black Pearl', 'Gore Verbinski', 2003, 'fantasy'),
                       ('Harry Potter and Goblet of Fire', 'Mike Newell', 2005, 'fantasy'),
                       ('The Hobbit: An Unexpected Journey', 'Peter Jackson', 2012, 'fantasy'),
                       ('Titanic', 'David Cameron', 1998, 'drame'),
                       ('Intouchables', 'Olivier Nakache', 2011, 'comedie');''')

conn.execute('''INSERT INTO patients (nom, prenom, age)
                VALUES ('Doe', 'John', 42),
                       ('Fontaine', 'Alice', 31);''')

# Fermer la connexion
conn.close()
