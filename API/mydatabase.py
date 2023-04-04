import sqlite3
import subprocess

# Exécuter la commande "sqlite3 mydatabase.db" dans le terminal
process = subprocess.Popen(['sqlite3', 'mydatabase.db'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# Envoyer la commande ".databases" à l'interpréteur SQLite
output, error = process.communicate('.databases\n'.encode())

# Afficher la sortie de la commande SQLite
print(output.decode())
