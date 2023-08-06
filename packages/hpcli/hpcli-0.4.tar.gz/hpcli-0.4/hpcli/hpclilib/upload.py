import io
import os
from zipfile import ZipFile
from hpcli.sdk.base import API
from shutil import make_archive
from .common import BACKEND_URL

# Thank you stack overflow


def zipdir(path, ziph):
    # ziph is zipfile handle
    # path is assumed to be the project name
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            arc_name = file_path.replace(path + '/', '')
            ziph.write(file_path, arc_name)


class MicroServiceUploader(object):
    def __init__(self, arguments, config):
        self.arguments = arguments
        self.config = config
        self.truncated_user_id = config['id'][0:6]
        self.project_root = self.arguments['<project-name>']
        self.project_zip_name = "%s-%s.zip" % (self.config['id'][0:6], self.arguments['<project-name>'])
        self.api = API('api/microservices/storage/microservice/',
                       override_url_root=BACKEND_URL)
        self.file_data = io.BytesIO()

    def _zip_project(self):
        ziph = ZipFile(self.file_data, 'w')
        zipdir(self.project_root, ziph)

    def _generate_doc_file_name(self, file_name):
        return "docs/%s/%s/%s" % (self.truncated_user_id, self.project_root, file_name)

    def upload(self):
        self._zip_project()
        return self.api.post(
            {},
            files={self.project_zip_name: self.file_data.getvalue()}
        )

    def upload_docs(self):
        self.api = API('api/microservices/storage/microservice-docs/',
                       override_url_root=BACKEND_URL)
        files = {}
        docs_folder = os.path.join(self.project_root, 'docs')
        if not os.path.exists(docs_folder):
            return
        for file_name in filter(lambda x: not x.startswith('.'),
                           os.listdir(docs_folder)):
            doc_file_name = self._generate_doc_file_name(file_name)
            with open(os.path.join(docs_folder, file_name), 'r') as f:
                files[doc_file_name] = f.read()
        return self.api.post(
            {},
            files=files
        )

