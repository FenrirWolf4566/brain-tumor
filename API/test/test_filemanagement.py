import requests
from testing_constants import *

# Run all the tests of this file from the project's root folder
# pytest -s -v API/test/test_filemanagement.py
# add ::test_name to select the specific test name

# The two following functions are supposed to work as expected
# They are tested in test_aut.py

def get_token(data):
    # authentication process 
    response = requests.post(url+'account/auth', headers=basic_headers, data=data).json()
    return response['access_token']

def disconnect(token):
    requests.get(url+'account/disconnect', headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'})

# It should not have pre-loaded files just after authentication
def test_empty_file_list_at_start():
    for data_auth in login_password_existing_users:
        token = get_token(data_auth)
        # request for file list
        file_list = requests.get(url+'files', headers={'accept': 'application/json', 'Authorization': f'Bearer {token}'}).json()['loaded_files']
        assert(file_list==[])
        disconnect(token)


def drop_file(filetype,token):
    file_path = f'./API/test/examples/example_1/example_1_{filetype}.nii.gz'
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}",
    }
    files = {"file": (file_path, open(file_path, "rb"), "application/x-gzip")}
    response = requests.post(url+'files/'+filetype, headers=headers, files=files)
    return response.json()

def assert_drop_file(filetype,response):
    loaded_files = response['loaded_files']
    assert(filetype in loaded_files)

# for each file type, connects, drops and disconnects
def test_drop_single_file():
    for filetype in filetypes:
        for data_auth in login_password_existing_users:
            token =get_token(data_auth)
            assert_drop_file(filetype,drop_file(filetype,token))
            disconnect(token)

# drops the 4 necessary files 
def test_drop_four_files():
    for data_auth in login_password_existing_users:
            token =get_token(data_auth)
            for filetype in filetypes:
                assert_drop_file(filetype,drop_file(filetype,token))
            disconnect(token)

# drops the same filetype twice 
def test_drop_same_file_twice():
    for data_auth in login_password_existing_users:
            token =get_token(data_auth)
            for filetype in filetypes:
                drop_1 = drop_file(filetype,token)
                assert_drop_file(filetype,drop_1)
                drop_2 = drop_file(filetype,token)
                assert_drop_file(filetype,drop_2)
                file_list_1=drop_1['loaded_files']
                file_list_2=drop_2['loaded_files']
                #the file list should be the same 
                #(the new file replaces the previous one) 
                assert(file_list_1==file_list_2)
            disconnect(token)

#TODO: tests cancel_files and analyse


