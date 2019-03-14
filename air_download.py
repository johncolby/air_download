import time
import json
import requests
from urllib.parse import urljoin

# url_top = 'https://air.<domain>.edu/api/'
# cred_path = 'air_login.txt'
# acc = '11111111'

with open(cred_path) as fd:
    userId, password = [x.strip() for x in fd.readlines()]

auth_info = {
    'userId': userId,
    'password': password
}

session = requests.post(urljoin(url_top, 'login'), json = auth_info).json()

jwt = session['token']['jwt']
header = {'Authorization': 'Bearer ' + jwt}

study = requests.post(urljoin(url_top, 'secure/search/query-data-source'), 
    headers = header,
    json = {'name': '',
            'mrn': '',
            'accNum': acc,
            'dateRange': {'start':'','end':'','label':''},
            'modality': '',
            'sourceId': 1
    }).json()['exams'][0]

series = requests.post(urljoin(url_top, 'secure/search/series'),
    headers = header,
    json = study).json()

def has_started():
    check = requests.post(urljoin(url_top, 'secure/search/download/check'),
        headers = header,
        json = {'downloadId': download_info['downloadId'],
            'projectId': -1
        }).json()
    return check['status'] in ['started', 'completed']

download_info = requests.post(urljoin(url_top, 'secure/search/download/start'),
    headers = header,
    json = {'decompress': False,
            'name': 'Download.zip',
            'profile': -1,
            'projectId': -1,
            'series': series,
            'study': study 
    }).json()

while not has_started():
    time.sleep(0.1)

download_stream = requests.post(urljoin(url_top, 'secure/search/download/zip'),
    headers = {'Upgrade-Insecure-Requests': '1'},
    data = {'params': json.dumps({'downloadId': download_info['downloadId'], 'projectId': -1, 'name': 'Download.zip'}),
            'jwt': jwt
    }, stream=True)

with open('Download.zip', 'wb') as fd:
    for chunk in download_stream.iter_content(chunk_size=8192):
        if chunk:
            _ = fd.write(chunk)