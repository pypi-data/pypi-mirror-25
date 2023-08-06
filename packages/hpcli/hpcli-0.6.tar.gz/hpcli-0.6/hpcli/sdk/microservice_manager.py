from .base import API
from requests.compat import urljoin
import os
import json

MS_DEPLOY_URL_FRAGMENT = 'highlyprobable/microservice'
DRF_URL_ROOT = "https://backend.api.highlyprobable.com/"



class MicroServiceManager(object):
    def __init__(self, arguments, config):
        self.config = config
        self.arguments = arguments
        self.url_fragment = MS_DEPLOY_URL_FRAGMENT
        self.truncated_user_id = config['id'][0:6]
        self.project_name = self.arguments['<project-name>']
        self.zip_name = "%s-%s.zip" % (self.config['id'][0:6], self.project_name)

    def _get_post_data(self, action):
        return {
            'user-id': self.truncated_user_id,
            'x-api-key': self.config['id'],
            'microservice-name': self.project_name,
            'cpu': self.config.get('cpu'),
            'memory': self.config.get('memory'),
            "module-location": "highly-probable-custom-microservices",
            "module-location-type": "s3",
            "module-name": self.zip_name,
            'action': action,
        }

    def _get_docs_data(self):
        docs_data = {
            "docs_url": "",
            "use_cases_url": "",
            "get_started_url": "",
        }
        docs_path = os.path.join(self.arguments['<project-name>'], 'docs')
        remote_url = "https://highlyprobable.com/docs/%s/%s/" % (
            self.truncated_user_id,
            self.project_name
        )
        docs_files = {
            'Documentation.ipynb': 'docs_url',
            'Getting-Started.ipynb': 'use_cases_url',
            'Use-Cases.ipynb': 'get_started_url',
        }
        if not os.path.isdir(docs_path):
            return docs_path
        for (doc_file, corr_url) in docs_files.items():
            file_path = os.path.join(docs_path, doc_file)
            if not os.path.exists(file_path):
                continue
            docs_data[corr_url] = remote_url + doc_file
        return docs_data

    def _get_default_image_url(self):
        if self.config.get('category').startswith('IMG'):
            return "https://highlyprobable.com/assets/icons/img.png"
        return "https://highlyprobable.com/assets/icons/nlp.png"

    def _get_drf_information(self):
        data = {}
        if 'backend-url' in self.config:
            data['url'] = self.config['backend-url']
        if 'backend-slug-name' in self.config:
            data['slug_name'] = self.config['backend-slug-name']
        return data

    def _get_drf_data(self):
        microservice_defn = self._get_post_data('')
        del microservice_defn['action']
        # TODO: Use slug_name here instead of calculating it
        api_url = self.config['id'][0:6] + '/' + self.config['microservice-name']

        return {
            "account_id": self.config.get('id'),
            "category": self.config.get('category', ''),
            "name": self.config.get('friendly_name', ''),
            "account": self.config['id'],
            "description": self.config.get('description', ''),
            "icon_url": self._get_default_image_url(),
            "source_code_url": "",
            "api_url": api_url,
            "microservice_definition": microservice_defn,
            "price": 1,
            "unit": 10000,
            "ratings": None,
            "comments": None,
            "is_used_by_account": False,
            **self._get_docs_data(),
            **self._get_drf_information(),
        }

    def _post_drf(self):
        api = API('api/microservices/microservice/',
                  override_url_root=DRF_URL_ROOT,
                  config=self.config)
        return api.post(self._get_drf_data())

    def _patch_drf(self):
        patch_url = self.config['backend-url']
        return API('',
                   full_url_override=patch_url,
                   config=self.config).patch(self._get_drf_data())

    def create_microservice(self):
        drf_data = {}
        if 'backend-url' not in self.config:
            drf_data = self._post_drf()
        else:
            drf_data = self._patch_drf()
        a = self._get_post_data('create')
        r = API(MS_DEPLOY_URL_FRAGMENT).post(a)
        return {'drf': drf_data, 'cluster': r}

    def start_microservice(self):
        a = self._get_post_data('start')
        r = API(MS_DEPLOY_URL_FRAGMENT).post(a)
        return r

    def stop_microservice(self):
        a = self._get_post_data('stop')
        r = API(MS_DEPLOY_URL_FRAGMENT).post(a)
        return r

