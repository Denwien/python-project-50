import json
from gendiff.formaters.stylish import format_diff_stylish

def load_file(path):
    """Загружает JSON-файл (добавьте YAML при необходимости)."""
    with open(path) as f:
        if path.endswith('.json'):
            return json.load(f)
        raise ValueError("Unsupported file type")

def build_diff(data1, data2):
    """Рекурсивно строит список изменений между двумя словарями."""
    diff = []
    keys = sorted(data1.keys() | data2.keys())
    for key in keys:
        val1 = data1.get(key)
        val2 = data2.get(key)
        if key not in data1:
            diff.append({"name": key, "action": "added", "value": val2, "children": []})
        elif key not in data2:
            diff.append({"name": key, "action": "deleted", "value": val1, "children": []})
        elif isinstance(val1, dict) and isinstance(val2, dict):
            diff.append({"name": key, "action": "nested", "value": None, "children": build_diff(val1, val2)})
        elif val1 != val2:
            diff.append({"name": key, "action": "deleted", "value": val1, "children": []})
            diff.append({"name": key, "action": "added", "value": val2, "children": []})
        else:
            diff.append({"name": key, "action": "unchanged", "value": val1, "children": []})
    return diff

def generate_diff(file1, file2, format_name='stylish'):
    data1 = load_file(file1)
    data2 = load_file(file2)
    diff = build_diff(data1, data2)
    if format_name == 'stylish':
        return format_diff_stylish(diff)
    return diff
