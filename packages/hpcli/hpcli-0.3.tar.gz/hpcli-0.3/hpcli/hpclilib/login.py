import os
import json
from getpass import getpass
from hpcli.sdk.auth import authenticate

AUTH_DIR = os.path.join(
    os.path.expanduser('~'),
    '.highlyprobable'
)

AUTH_FILE_NAME_PATH = os.path.join(
    AUTH_DIR,
    'credentials'
)


def write_auth_file(json_data):
    try:
        os.mkdir(AUTH_DIR)
    except OSError:
        pass
    with open(AUTH_FILE_NAME_PATH, 'w') as f:
        f.write(json.dumps(json_data))


def login_post(data):
    post_res = authenticate(data)
    if 'error' not in post_res:
        write_auth_file(post_res)
        return True
    return False


def interactive_login():
    data = {
        'email': input("Please enter your email: "),
        'password': getpass("Please enter your password: ")
    }
    return login_post(data)


def is_logged_in():
    if not os.path.exists(AUTH_FILE_NAME_PATH):
        return False
    return True


def load_credentials(project_root, project_name):
    config = {}
    if os.path.exists(AUTH_FILE_NAME_PATH):
        with open(AUTH_FILE_NAME_PATH) as f:
            auth_data = json.load(f)
            config = {**config, **auth_data}
    else:
        raise RuntimeError('Authentication file not found, try `hpcli login`.')
    microserice_defn_file = os.path.join(project_root, 'microservice-definition.json')
    if os.path.exists(microserice_defn_file):
        with open(microserice_defn_file) as f:
            config_data = json.load(f)
            config = {**config, **config_data}
    elif os.path.exists(project_root):
        missing_info = {}
        missing_info['cpu'] = 200
        missing_info['mem'] = 350
        missing_info['microservice-name'] = project_name
        with open(microserice_defn_file, 'w') as f:
            f.write(json.dumps(missing_info, indent=4, sort_keys=True))
        config = {**config, **missing_info}
    return config
