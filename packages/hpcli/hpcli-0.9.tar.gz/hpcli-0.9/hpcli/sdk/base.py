import requests
import json
from requests.compat import urljoin
from hpcli.hpclilib.common import MS_URL_ROOT


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

        self.x_api_key = ""
        if config and 'id' in config:
            self.x_api_key = self.config['id']
        elif api_key:
            self.x_api_key = api_key

        self.auth_token = ""
        if config and 'token' in config:
            self.auth_token = config['token']

    def _determine_headers(self, data):
        headers = {}
        if 'get' in dir(data) and not self.x_api_key:
            self.x_api_key = data.get('x-api-key', "")
        headers = {
            'x-api-key': self.x_api_key,
        }
        if self.auth_token:
            headers['Authorization'] = "Token %s" % self.auth_token
        if type(data) == bytes:
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return headers

    def _determine_request_params(self, data, files=None):
        if files:
            return {'files': files}
        if type(data) == bytes:
            return {'data': data}
        return {'json': data}

    def _handle_res(self, res):
        try:
            return json.loads(res.text)
        except:
            return res.text

    def post(self, data, files=None):
        headers = self._determine_headers(data)
        res = requests.post(
            self.url,
            **self._determine_request_params(data, files=files)
        )
        return self._handle_res(res)

    def get(self, data):
        headers = self._determine_headers(data)
        res = requests.get(self.url, headers=headers)
        return res.text

    def patch(self, data):
        headers = self._determine_headers(data)
        res = requests.patch(
            self.url,
            **self._determine_request_params(data)
        )
        return self._handle_res(res)
