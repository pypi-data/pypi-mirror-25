import requests
import json
from requests.compat import urljoin

MS_URL_ROOT = "https://u2b27vbv1j.execute-api.us-east-1.amazonaws.com/prod/1/"


class API(object):
    def __init__(self,
                 url_fragment,
                 api_key=None,
                 override_url_root=None,
                 config=None,
                 full_url_override=None):
        self.url_fragment = url_fragment
        self.url_root = MS_URL_ROOT
        self.config = config

        if override_url_root:
            self.url_root = override_url_root

        if full_url_override:
            self.url = full_url_override
        else:
            self.url = urljoin(self.url_root, self.url_fragment)

        self.x_api_key = None
        if config and 'id' in config:
            self.x_api_key = self.config['id']
        elif api_key:
            self.x_api_key = api_key

        self.auth_token = ""
        if config and 'token' in config:
            self.auth_token = config['token']

    def _determine_headers(self, json_data):
        headers = {}
        if not self.x_api_key:
            self.x_api_key = json_data.get('x-api-key', "")
        headers = {
            'x-api-key': self.x_api_key,
        }
        if self.auth_token:
            headers['Authorization'] = "Token %s" % self.auth_token
        return headers

    def _handle_res(self, res):
        try:
            return json.loads(res.text)
        except:
            return res.text

    def post(self, json_data, files=None):
        headers = self._determine_headers(json_data)
        res = requests.post(self.url,
                            headers=headers,
                            json=json_data,
                            files=files)
        return self._handle_res(res)

    def get(self, json_data):
        headers = self._determine_headers(json_data)
        res = requests.get(self.url, headers=headers)
        return res.text

    def patch(self, json_data):
        headers = self._determine_headers(json_data)
        res = requests.patch(self.url,
                             headers=headers,
                             json=json_data)
        return self._handle_res(res)
