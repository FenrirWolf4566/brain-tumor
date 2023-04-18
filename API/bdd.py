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

def create_user(conn : sqlite3.Connection, id, username, full_name, email, hashed_password):
    conn.execute(f'''INSERT INTO comptes (id, username, full_name, email, hashed_password)
                     VALUES ('{id}', '{username}', '{full_name}', '{email}', '{hashed_password}')''')
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
    fake_users_db = {
    "johndoe": {
        "id":"1",
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("bonjour"),
    },
    "alicefontaine": {
        "id":"2",
        "username": "alicefontaine",
        "full_name": "Alice Fontaine",
        "email": "alicefontaine@example.com",
        "hashed_password": pwd_context.hash("salut"),
    },
    "johannbourcier": {
        "id":"3",
        "username": "johann",
        "full_name": "Johann Bourcier",
        "email": "johannbourcier@example.com",
        "hashed_password": pwd_context.hash("bourcier"),
    },
    "francescagalassi": {
        "id":"4",
        "username": "francesca",
        "full_name": "Francesca Galassi",
        "email": "francescagalassi@example.com",
        "hashed_password": pwd_context.hash("galassi"),
    },
    "hélènefeuillatre": {
        "id":"5",
        "username": "helene",
        "full_name": "Helene Feuillatre",
        "email": "helenefeuillatre@example.com",
        "hashed_password": pwd_context.hash("feuillatre"),
    }
    }
    con = get_conn("doctors.db")
    create_comptes_table(con)
    john = fake_users_db["johndoe"]
    alice= fake_users_db["alicefontaine"]
    johann= fake_users_db["johannbourcier"]
    create_user(con,john['id'],john['username'],john['full_name'],john['email'],john['hashed_password'])
    create_user(con,alice['id'],alice['username'],alice['full_name'],alice['email'],alice['hashed_password'])
    create_user(con,johann['id'],johann['username'],johann['full_name'],johann['email'],johann['hashed_password'])
    return get_users(con)

