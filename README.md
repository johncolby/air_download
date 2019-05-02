# Automated Image Retrieval (AIR) Download

This is a small wrapper interface to the AIR web API. This will help you to batch download radiology studies if you have this service available on your PACS system.

## Install

1. Clone repository.

    ```bash
    git clone https://github.com/johncolby/air_download
    ```

1. Make sure `python` is installed.

    ```bash
    python --version
    ```

1. Install `requests` python dependency, if not already available. For example:

    ```bash
    pip install requests
    ```

## Usage

```
cd /path/to/air_download/
./air_download.py -c /path/to/air_login.txt https://air.<domain>.edu/api/ 11111111
```

Login credentials should be stored in a plain text file like:
```
username
password
```

Please ensure this file is reasonably secure.

```bash
chmod 600 air_login.txt
```

Type `air_download.py -h` for the help text.

```
$ air_download.py -h
usage: air_download.py [-h] [-c CRED_PATH] [-p PROFILE] [-o OUTPUT]
                       URL ACCESSION

positional arguments:
  URL                   URL for AIR API, e.g. https://air.<domain>.edu/api/
  ACCESSION             Accession # to download

optional arguments:
  -h, --help            show this help message and exit
  -c CRED_PATH, --cred_path CRED_PATH
                        Login credentials file (default: ./air_login.txt)
  -p PROFILE, --profile PROFILE
                        Anonymization Profile (default: -1)
  -o OUTPUT, --output OUTPUT
                        Output path (default: ./<Accession>.zip)
```