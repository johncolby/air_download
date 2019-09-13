import os
import argparse
import time
import json
import requests
from dotenv import dotenv_values
from urllib.parse import urljoin

def parse_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('URL', help='URL for AIR API, e.g. https://air.<domain>.edu/api/')
    parser.add_argument('acc', metavar='ACCESSION', help='Accession # to download')
    parser.add_argument('-c', '--cred_path', help='Login credentials file. If not present, will look for AIR_USERNAME and AIR_PASSWORD environment variables.', default=None)
    parser.add_argument('-p', '--profile', help='Anonymization Profile', default=-1)
    parser.add_argument('-o', '--output', help='Output path', default='./<Accession>.zip')

    arguments = parser.parse_args()

    if arguments.output == './<Accession>.zip':
        arguments.output = '{acc}.zip'.format(acc=arguments.acc)

    return arguments

def main(args):
    # Import login credentials
    if args.cred_path is None:
        userId   = os.environ.get('AIR_USERNAME')
        password = os.environ.get('AIR_PASSWORD')
        assert((userId and password) is not None), "AIR credentials not provided."
    else:
        assert(os.path.exists(args.cred_path)), f'AIR credential file ({args.cred_path}) does not exist.'
        envs = dotenv_values(args.cred_path)
        userId = envs['AIR_USERNAME']
        password = envs['AIR_PASSWORD']  
    auth_info = {
        'userId': userId,
        'password': password
    }

    # Initialize AIR session and store authorization token
    session = requests.post(urljoin(args.URL, 'login'), json = auth_info).json()

    jwt = session['token']['jwt']
    header = {'Authorization': 'Bearer ' + jwt}

    # Search for study by accession number 
    study = requests.post(urljoin(args.URL, 'secure/search/query-data-source'), 
        headers = header,
        json = {'name': '',
                'mrn': '',
                'accNum': args.acc,
                'dateRange': {'start':'','end':'','label':''},
                'modality': '',
                'sourceId': 1
        }).json()['exams'][0]

    # Make a list of all included series
    series = requests.post(urljoin(args.URL, 'secure/search/series'),
        headers = header,
        json = study).json()

    def has_started():
        check = requests.post(urljoin(args.URL, 'secure/search/download/check'),
            headers = header,
            json = {'downloadId': download_info['downloadId'],
                'projectId': -1
            }).json()
        return check['status'] in ['started', 'completed']

    # Prepare download job
    download_info = requests.post(urljoin(args.URL, 'secure/search/download/start'),
        headers = header,
        json = {'decompress': False,
                'name': 'Download.zip',
                'profile': args.profile,
                'projectId': -1,
                'series': series,
                'study': study 
        }).json()

    # Ensure that archive is ready for download
    while not has_started():
        time.sleep(0.1)

    # Download archive
    download_stream = requests.post(urljoin(args.URL, 'secure/search/download/zip'),
        headers = {'Upgrade-Insecure-Requests': '1'},
        data = {'params': json.dumps({'downloadId': download_info['downloadId'], 'projectId': -1, 'name': 'Download.zip'}),
                'jwt': jwt
        }, stream=True)

    # Save archive to disk
    with open(args.output, 'wb') as fd:
        for chunk in download_stream.iter_content(chunk_size=8192):
            if chunk:
                _ = fd.write(chunk)

def cli():
    main(parse_args())
