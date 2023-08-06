from .base import API
from requests.compat import urljoin

MS_DEPLOY_URL_FRAGMENT = 'highlyprobable/microservice'
DRF_URL_ROOT = "https://backend.api.highlyprobable.com/"


class MicroServiceManager(object):
    def __init__(self, arguments, config):
        self.config = config
        self.arguments = arguments
        self.url_fragment = MS_DEPLOY_URL_FRAGMENT
        self.truncated_user_id = config['id'][0:6]
        self.zip_name = "%s-%s.zip" % (self.config['id'][0:6], self.arguments['<project-name>'])

    def _get_post_data(self, action):
        return {
            'user-id': self.truncated_user_id,
            'x-api-key': self.config['id'],
            'microservice-name': self.arguments['<project-name>'],
            'cpu': self.config.get('cpu'),
            'memory': self.config.get('memory'),
            "module-location": "highly-probable-custom-microservices",
            "module-location-type": "s3",
            "module-name": self.zip_name,
            'action': action,
        }

    def _get_drf_data(self):
        microservice_defn = self._get_post_data('')
        del microservice_defn['action']
        api_url = self.config['id'][0:6] + '/' + self.config['microservice-name']

        return {
            "account_id": self.config.get('id'),
            "category": self.config.get('category', ''),
            "name": self.config.get('friendly_name', ''),
            "account": self.config['id'],
            "description": self.config.get('description', ''),
            "icon_url": "",
            "source_code_url": "",
            "docs_url": "",
            "use_cases_url": "",
            "get_started_url": "",
            "api_url": api_url,
            "microservice_definition": microservice_defn,
            "price": 1,
            "unit": 10000,
            "ratings": None,
            "comments": None,
            "is_used_by_account": False,
        }

    def _post_drf(self):
        api = API('api/microservices/microservice/',
                  override_url_root=DRF_URL_ROOT,
                  config=self.config)
        rrr = api.post(self._get_drf_data())
        print(rrr)

    def create_microservice(self):
        self._post_drf()
        a = self._get_post_data('create')
        r = API(MS_DEPLOY_URL_FRAGMENT).post(a)
        return r

    def start_microservice(self):
        a = self._get_post_data('start')
        r = API(MS_DEPLOY_URL_FRAGMENT).post(a)
        return r

    def stop_microservice(self):
        a = self._get_post_data('stop')
        r = API(MS_DEPLOY_URL_FRAGMENT).post(a)
        return r

