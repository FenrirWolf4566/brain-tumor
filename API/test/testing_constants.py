# constants used for testing the API

# API endpoint URL
url = "http://localhost:8000/"

# Header for a query with no authentication
basic_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# false users that are loaded by default in the API
login_password_existing_users = [
    {
        'username': 'johndoe',
        'password': 'bonjour',
    },
    {
        'username': 'alicefontaine',
        'password': 'salut'
    }
]

# informations about those false users
info_existing_users = [
    {
        "id": 1,
        "username": "johndoe",
        "email": "johndoe@example.com",
        "full_name": "John Doe",
        "res_status": "success"
    },
    {
        "id": 2,
        "username": "alicefontaine",
        "email": "alicefontaine@example.com",
        "full_name": "Alice Fontaine",
        "res_status": "success"
    }
]

filetypes =['t1','t1ce','t2','flair']