import json
import yaml

def load_file(file_path: str):
    """Загружает JSON или YAML файл в словарь."""
    if file_path.endswith('.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif file_path.endswith(('.yml', '.yaml')):
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
