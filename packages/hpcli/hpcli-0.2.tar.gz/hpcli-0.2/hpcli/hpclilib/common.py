import os

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
