import sqlite3

def loadTables():
    con = sqlite3.connect("matable.db")
    cur = con.cursor()
    res = cur.execute("SELECT * FROM patients")
    patients = res.fetchall()
    res = cur.execute("SELECT * FROM movies")
    comptes = res.fetchall()
    print(patients)
    print(comptes)
    cur.close()

loadTables()