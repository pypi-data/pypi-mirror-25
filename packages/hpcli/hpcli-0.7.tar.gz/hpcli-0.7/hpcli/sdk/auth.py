from .base import API
from hpcli.hpclilib.common import DRF_URL_ROOT, AUTH_URL_PATH

def authenticate(username_password):
    return API(AUTH_URL_PATH, override_url_root=DRF_URL_ROOT).post(username_password)
