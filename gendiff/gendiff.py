import json
import yaml

def load_file(filepath):
    """Загружает JSON или YAML файл и возвращает словарь."""
    with open(filepath) as f:
        if filepath.endswith('.json'):
            return json.load(f)
        elif filepath.endswith(('.yml', '.yaml')):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format")

def build_diff(data1, data2):
    """Рекурсивно строит список изменений."""
    keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff = []

    for key in keys:
        if key not in data1:
            diff.append({"name": key, "action": "added", "value": data2[key]})
        elif key not in data2:
            diff.append({"name": key, "action": "deleted", "value": data1[key]})
        else:
            val1 = data1[key]
            val2 = data2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                children = build_diff(val1, val2)
                diff.append({"name": key, "action": "nested", "children": children})
            elif val1 != val2:
                diff.append({"name": key, "action": "modified", "old_value": val1, "new_value": val2})
            else:
                diff.append({"name": key, "action": "unchanged", "value": val1})
    return diff

def generate_diff(file1, file2, format_name="stylish"):
    """Главная функция генерации diff."""
    data1 = load_file(file1)
    data2 = load_file(file2)
    diff_list = build_diff(data1, data2)

    if format_name == "stylish":
        from gendiff.formaters.stylish import format_diff_stylish
        return format_diff_stylish(diff_list)
    else:
        raise ValueError("Unknown format")


