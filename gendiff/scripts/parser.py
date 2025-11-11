import json
import yaml
import os


def parse_data_from_file(file_path):
    _, extension = os.path.splitext(file_path)

    with open(file_path) as file:
        if extension in ('.yaml', '.yml'):
            return yaml.safe_load(file)
        elif extension == '.json':
            return json.load(file)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
