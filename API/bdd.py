import sqlite3

# Établir une connexion à la base de données
def get_conn(database_name):
    return sqlite3.connect(database_name)

def create_comptes_table(conn):
    conn.execute('DROP TABLE IF EXISTS comptes;')
    conn.execute('''CREATE TABLE comptes (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    username         TEXT,
                    full_name        TEXT,
                    email            TEXT,
                    hashed_password  TEXT
                  );''')

def close_connection(conn):
    conn.close()

def create_user(conn : sqlite3.Connection, username, full_name, email, hashed_password):
    conn.execute(f'''INSERT INTO comptes (username, full_name, email, hashed_password)
                     VALUES ('{username}', '{full_name}', '{email}', '{hashed_password}')''')
    conn.commit()

def get_users(conn : sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comptes;')
    users_list = cursor.fetchall()
    users={}
    for user in users_list:
        id_,username_,full_name_,email_,hashed_password_ = user
        users[username_]={
            'id':id_,
            'username':username_,
            'full_name':full_name_,
            'email':email_,
            'hashed_password':hashed_password_
        }
    return users



def initiateBasicDb(pwd_context):
    con = get_conn("doctors.db")
    create_comptes_table(con)
    create_user(con,"johndoe","John Doe","johndoe@example.com", pwd_context.hash("bonjour"))
    create_user(con,"alicefontaine","Alice Fontaine","alicefontaine@example.com",pwd_context.hash("salut"))
    create_user(con,"johann","Johann Bourcier","johannbourcier@irisa.fr",pwd_context.hash("bourcier"))
    create_user(con,"francesca","Francesca Galassi","francescagalassi@irisa.fr",pwd_context.hash("galassi"))
    create_user(con,"helene","Helene Feuillatre","helenefeuillatre@irisa.fr",pwd_context.hash("feuillatre"))
    return get_users(con)