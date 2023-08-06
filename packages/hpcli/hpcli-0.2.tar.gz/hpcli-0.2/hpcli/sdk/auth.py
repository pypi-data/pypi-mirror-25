from .base import API

AUTH_URL_PATH = 'api/organizations/api-token-auth/'
AUTH_URL_ROOT = "https://backend.api.highlyprobable.com/"


def authenticate(username_password):
    return API(AUTH_URL_PATH, override_url_root=AUTH_URL_ROOT).post(username_password)
