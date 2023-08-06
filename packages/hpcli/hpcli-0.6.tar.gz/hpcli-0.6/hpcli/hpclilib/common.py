import os
import json
from hpcli.sdk.base import MS_URL_ROOT
from requests.compat import urljoin

DOCKER_REPO_URLS = {
    'python3-generic': 'dpbriggs/python3-generic',
}

MODULE_ROOT = os.path.dirname(os.path.abspath(__file__))
BIG_SEP = '=' * 80
BACKEND_URL = "https://backend.api.highlyprobable.com/"

def big_print(to_print, first_print=False):
    if first_print:
        print('')
    print(BIG_SEP)
    print('')
    print(to_print)
    print('')


def get_project_root(arguments):
    return os.path.join(os.getcwd(), arguments['<project-name>'])


def get_short_id(config):
    return config['id'][0:6]


def find_project_url_fragment(config, full_path=True):
    url = ""
    if 'id' in config and 'microservice-name' in config:
        if full_path:
            url = urljoin(MS_URL_ROOT, config['id'][0:6]) + '/'
            url = urljoin(url, config['microservice-name'])
        else:
            url = config['id'][0:6] + '/' + config['microservice-name']
    elif not url:
        raise ValueError('Cannot find a suitable url, did you start the project?')
    return url


def add_to_microservice_defn_file(project_root, to_add):
    microserice_defn_file = os.path.join(project_root, 'microservice-definition.json')
    if not os.path.exists(microserice_defn_file):
        return
    json_data = {}
    with open(microserice_defn_file, 'rb') as f:
        json_data = json.loads(f.read())
    json_data = {**json_data, **to_add}
    with open(microserice_defn_file, 'w') as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True))
