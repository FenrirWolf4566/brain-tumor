from datetime import datetime
import requests

# To run these tests, make sure to have pytest installed
# then run in command line  pytest -s

# API endpoint URL
url = "http://localhost:8000/"

basic_headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

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


# Init test in order to check if the api is reachable
def test_access_to_api():
    response = requests.get(url)
    assert (response.status_code == 200)
    assert (response.json()['message'] == 'Hello World')

# The registered user authenticates with the good login and password
def test_usual_auth():
    for data in login_password_existing_users:
        response = requests.post(
            url+'account/auth', headers=basic_headers, data=data)
        assert (response.status_code == 200)
        response_data = response.json()
        # The authentication happened well
        assert (response_data['res_status'] == 'success')
        # The access token is valid
        assert (len(response_data['access_token']) > 0)
        # The given token is valid
        assert (datetime.strptime(
            response_data['expires'], '%Y-%m-%dT%H:%M:%S.%f') > datetime.now())

# Asserts for every wrong kind of authentication
def asserts_auth_failure(data):
    response = requests.post(url+'account/auth', headers=basic_headers, data=data)
    assert (response.status_code == 200)
    response_data = response.json()
    assert (response_data['res_status'] == 'error')


def test_wrong_username_right_password():
    data = {
        'username': 'wrongusername',
        'password': 'bonjour',
    }
    asserts_auth_failure(data)


def test_right_username_wrong_password():
    data = {
        'username': 'johndoe',
        'password': 'wrongpassword',
    }
    asserts_auth_failure(data)


def test_wrong_username_wrong_password():
    data = {
        'username': 'wrongusername',
        'password': 'wrongpassword',
    }
    asserts_auth_failure(data)

def authenticated_endpoint_response(endpoint,data_auth):
    # authenticate and obtain access token
    response = requests.post(url+'account/auth', headers=basic_headers, data=data_auth )
    return requests.get(url+endpoint, headers={'accept': 'application/json','Authorization': f'Bearer {response.json()["access_token"]}'})
    

# Basic asserts accessing to an endpoint requiring to be authenticated
def asserts_access_locked_endpoint(response):
    assert response.status_code == 200
    response_data = response.json()
    assert(response_data['res_status']=='success')
    

# Checking if the authenticated users to have access to their personal data
def test_user_authenticated_personal_info():
    for i,data in enumerate(login_password_existing_users):    
        response = authenticated_endpoint_response('account/me',data)
        asserts_access_locked_endpoint(response)
        response_data = response.json()
        assert(response_data==info_existing_users[i])

# If the given token is wrong people should not have access to their personal data
def test_user_not_authenticated_personal_info():
    random_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwiZXhwIjoxNjgyNzc1MDIzfQ.GybJ_lG-vZ0NaFRMeuovY3DZ_bInISLtbGzjr_B1HbM' # outdated jwt token (should never be valid again). 
    response= requests.get(url+'account/me', headers={'accept': 'application/json','Authorization': f'Bearer {random_token}'})
    assert(response.status_code==200)
    assert(response.json()['res_status']=='error')

# Checking if deauthentication works as expected
def test_disconnect():
    for data in  login_password_existing_users:    
        response = authenticated_endpoint_response('account/disconnect',data)
        asserts_access_locked_endpoint(response)
        response_data = response.json()
        assert(response_data['res_status']=='success')