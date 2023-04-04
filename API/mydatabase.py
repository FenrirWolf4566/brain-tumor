import sqlite3

con = sqlite3.connect("matable.db")
cur = con.cursor()
sql_file = open("creationtable.sql")
cur.executescript(sql_file.read())
con.commit()
