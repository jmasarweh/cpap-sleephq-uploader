import requests
import hashlib
import os
import sys
import pathlib
import json
from collections import defaultdict, OrderedDict
import time
from dotenv import load_dotenv  # For loading environment variables

# Load environment variables

load_dotenv()

# ################################################################################################
# You must install python3 for macOS 10.9 and later	. https://www.python.org/downloads/macos/
# You also must change the variables and Id in the .env file, which will be called below
# # #################################################################################################

team_id = os.getenv('TEAM_ID')
device_id = os.getenv('DEVICE_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
sub_path = os.getenv('SUB_PATH')
dir_path = os.getenv('DIR_PATH')
print(client_id, client_secret, sub_path, dir_path)

def get_access_token(client_id, client_secret):
    url = "https://sleephq.com/oauth/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'password',
        'scope': 'read write'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        print("Authorization successful")
        return 'Bearer ' + response.json()['access_token']
    except requests.RequestException as e:
        print(f"Failed to get access token: {e}")
        sys.exit(1)


def calculate_md5(file_path):
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def collect_files(dir_path, sub_path):
    all_files = [file for file in pathlib.Path(dir_path).rglob("*") if file.is_file() and not file.name.startswith('.')]
    import_files = defaultdict(list)
    for file in all_files:
        long_path = os.path.abspath(file.parent)
        final_path = long_path.replace(sub_path, '.')
        import_files['path'].append(final_path + '/' + file.name)
        import_files['name'].append(file.name)
        import_files['content_hash'].append(calculate_md5(file))
    return import_files


def reserve_import_id(team_id, authorization):
    url = f"https://sleephq.com/api/v1/teams/{team_id}/imports"
    headers = {'Authorization': authorization, 'Accept': 'application/json'}
    payload = {'programatic': False}
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()['data']['id']
    except requests.RequestException as e:
        print(f"Failed to reserve import ID: {e}")
        sys.exit(1)


def upload_files(import_id, authorization, final_import_files_list, dir_path):
    url = f"https://sleephq.com/api/v1/imports/{import_id}/files"
    headers = {'Authorization': authorization}
    for value in final_import_files_list:
        os_path = str(value['path']).strip("./")
        file_path = os.path.join(dir_path, os_path)
        payload = value
        files = [('file', (value['name'], open(file_path, 'rb'), 'application/octet-stream'))]
        try:
            response = requests.post(url, headers=headers, data=payload, files=files)
            response.raise_for_status()
            print(f"File {value['name']} has been imported")
        except requests.RequestException as e:
            print(f"Failed to upload file {value['name']}: {e}")
            sys.exit(1)
        time.sleep(1.5)


def process_imported_files(import_id, authorization):
    url = f"https://sleephq.com/api/v1/imports/{import_id}/process_files"
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json'
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(f"Files are now being processed in SleepHQ for Import ID: {import_id}")
    except requests.RequestException as e:
        print(f"Failed to process imported files: {e}")
        print(f"But you can try the Process Import request again later by calling: {url}")
        sys.exit(1)


# Main workflow
authorization = get_access_token(client_id, client_secret)
import_files = collect_files(dir_path, sub_path)
ordered_import_files = [OrderedDict([('path', t), ('name', d), ('content_hash', c)]) for t, d, c in
                        zip(import_files['path'], import_files['name'], import_files['content_hash'])]
final_import_files_list = json.loads(json.dumps(ordered_import_files))
import_id = reserve_import_id(team_id, authorization)
upload_files(import_id, authorization, final_import_files_list, dir_path)
process_imported_files(import_id, authorization)
