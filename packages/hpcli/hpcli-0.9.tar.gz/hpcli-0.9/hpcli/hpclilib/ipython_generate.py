from hpcli.hpclilib.common import find_project_url_fragment
import nbformat
import os


class IPythonGenerate(object):
    """
    Generate generic iPython notebook files
    for template creation.
    """

    def __init__(self, arguments, config):
        self.url_fragment = find_project_url_fragment(config, full_path=False)
        self.doc_iden = self.url_fragment.replace('/', '-')
        self.arguments = arguments
        self.config = config
        self.file_path = os.path.join(arguments['<project-name>'], 'docs')
        self._make_doc_folder()

    def _format_code_cell(self, python_str):
        contents = [
            "from hpcli import HighlyProbable as HP",
            "",
            "input_data = {'text': 'hello world'}",
            ""
            "hp = HP('%s', api_key='YOUR_SECRET_CODE')" % self.url_fragment,
        ]
        if python_str:
            contents.append(python_str)
        return nbformat.v4.new_code_cell("\n".join(contents))

    def _make_doc_folder(self):
        try:
            os.mkdir(self.file_path)
        except FileExistsError:
            pass

    def _get_full_file_path(self, start):
        file_name = "%s.ipynb" % start
        return os.path.join(self.file_path, file_name)

    def write_getting_started(self):
        self.write_template('Getting-Started')

    def write_documentation(self):
        self.write_template('Documentation')

    def write_use_cases(self):
        self.write_template('Use-Cases')

    def write_template(self, file_start):
        nb = nbformat.v4.new_notebook()
        getting_started_fp = self._get_full_file_path(file_start)
        nb['cells'] = [self._format_code_cell('')]
        with open(getting_started_fp, 'w') as f:
            nbformat.write(nb, f)

    def write_all(self):
        self.write_getting_started()
        self.write_use_cases()
        self.write_documentation()
