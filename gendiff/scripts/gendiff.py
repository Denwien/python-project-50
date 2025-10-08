import json
from pathlib import Path
import yaml


def read_file(file_path):
    """Читает JSON или YAML файл и возвращает словарь."""
    path = Path(file_path)
    ext = path.suffix.lower()

    with path.open(encoding="utf-8") as f:
        if ext == ".json":
            return json.load(f)
        elif ext in (".yml", ".yaml"):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {ext}")


def build_diff(dict1, dict2):
    """Сравнивает два словаря и возвращает список изменений."""
    keys = sorted(dict1.keys() | dict2.keys())
    diff = []

    for key in keys:
        if key not in dict1:
            diff.append({"key": key, "status": "added", "value": dict2[key]})
        elif key not in dict2:
            diff.append({"key": key, "status": "removed", "value": dict1[key]})
        else:
            val1, val2 = dict1[key], dict2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                children = build_diff(val1, val2)
                diff.append({"key": key, "status": "nested", "children": children})
            elif val1 == val2:
                diff.append({"key": key, "status": "unchanged", "value": val1})
            else:
                diff.append({
                    "key": key,
                    "status": "changed",
                    "old_value": val1,
                    "new_value": val2,
                })
    return diff


def format_diff(diff, depth=0):
    """Форматирует diff в строку с отступами и префиксами."""
    indent = "  " * depth
    lines = ["{"]
    for item in diff:
        key = item["key"]
        status = item["status"]

        if status == "added":
            lines.append(f"{indent}  + {key}: {item['value']}")
        elif status == "removed":
            lines.append(f"{indent}  - {key}: {item['value']}")
        elif status == "unchanged":
            lines.append(f"{indent}    {key}: {item['value']}")
        elif status == "changed":
            lines.append(f"{indent}  - {key}: {item['old_value']}")
            lines.append(f"{indent}  + {key}: {item['new_value']}")
        elif status == "nested":
            children_str = format_diff(item["children"], depth + 2)
            lines.append(f"{indent}    {key}: {children_str}")
    lines.append(f"{indent}}}")
    return "\n".join(lines)


def generate_diff(file_path1, file_path2):
    """Основная функция для генерации diff двух файлов."""
    dict1 = read_file(file_path1)
    dict2 = read_file(file_path2)
    diff = build_diff(dict1, dict2)
    return format_diff(diff)


































