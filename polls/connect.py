import dropbox
from django.conf import settings
import requests
import json
import datetime

TOKEN_URL = 'https://api.dropbox.com/oauth2/token'
APP_KEY = 'naifizow6uxwbwc'
APP_SECRET = 'wrsutnvek2yg5s0'
AUTHORIZATION_CODE = 'BygxikU8iA4AAAAAAAAAXU4pVYE1JllnmFNNa-G-jZU'

import os
import requests
import datetime

APP_KEY = ''
APP_SECRET = ''
REFRESH_TOKEN = ''
TOKEN_FILE = ''

def save_token(access_token, retrieval_time):
    with open(TOKEN_FILE, 'w') as file:
        json.dump({
            'access_token': access_token,
            'retrieval_time': str(datetime.datetime.now())
        }, file)

def load_token():
    try:
        with open(TOKEN_FILE, 'r') as file:
            data = json.load(file)
            return data['access_token'], datetime.datetime.fromisoformat(data['retrieval_time'])
    except FileNotFoundError:
        return None, None

def refresh_access_token():
    url = "https://api.dropbox.com/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": APP_KEY,
        "client_secret": APP_SECRET
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        new_access_token = response.json().get("access_token")
        return new_access_token
    else:
        print("Failed to refresh access token")
        return None

def get_valid_access_token():
    access_token, retrieval_time = load_token()
    if access_token and retrieval_time:
        current_time = datetime.datetime.now()
        print(current_time)
        time_difference = current_time - retrieval_time
        print(time_difference)

        if time_difference.total_seconds() < 3 * 3600:  # 3 hours
            return access_token
    
    new_access_token = refresh_access_token()
    if new_access_token:
        save_token(new_access_token, datetime.datetime.now().isoformat())
        return new_access_token

    return None
 
def upload_image_to_dropbox(file, file_name):
    access_token = get_valid_access_token()
    dbx = dropbox.Dropbox(access_token)
    dbx.files_upload(file.read(), f'/{file_name}', mode=dropbox.files.WriteMode.overwrite)
    link = dbx.sharing_create_shared_link(f'/{file_name}')
    return link.url.replace('?dl=0', '?raw=1')

# def delete_file_from_dropbox(file_path):
#     ACCESS_TOKEN = 'sizning_access_tokeningiz'
#     dbx = dropbox.Dropbox(ACCESS_TOKEN)

#     try:
#         dbx.files_delete_v2(file_path)
#         return True
#     except dropbox.exceptions.ApiError as err:
#         return False

