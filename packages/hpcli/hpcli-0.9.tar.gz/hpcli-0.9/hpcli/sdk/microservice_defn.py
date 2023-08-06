import json
import os

class MicroServiceDefinition(object):
    def __init__(self, arguments, config):
        self.arguments = arguments
        self.config = config

    def to_dict(self):
        return {
            "microservice-name": self.arguments.get('<project-name>', 'echo'),
            "cpu": self.config.get('cpu', 300),
            "memory": self.config.get('memory', 350),
            "friendly-name": self.config.get('friendly-name', ''),
            "icon-url": self.config.get('icon-url', ''),
            "category": self.config.get('category', ''),
            "description": self.config.get('description', ''),
        }

    def write_to_file(self, path=None):
        project_name = self.arguments.get('<project-name>')
        if not path:
            path = project_name
        file_path = os.path.join(project_name, 'microservice-definition.json')
        with open(file_path, 'w') as f:
            f.write(json.dumps(self.to_dict(), indent=4, sort_keys=True))
