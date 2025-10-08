import json
import yaml
from pathlib import Path

def read_file(file_path):
    """Чтение данных из JSON или YAML файла."""
    path = Path(file_path)
    if path.suffix in ['.json']:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    elif path.suffix in ['.yml', '.yaml']:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")

def generate_diff_dict(data1, data2):
    """Рекурсивное сравнение двух словарей."""
    diff = {}
    keys = sorted(data1.keys() | data2.keys())
    for key in keys:
        if key not in data1:
            diff[key] = ('added', data2[key])
        elif key not in data2:
            diff[key] = ('removed', data1[key])
        else:
            val1, val2 = data1[key], data2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                nested = generate_diff_dict(val1, val2)
                diff[key] = ('nested', nested)
            elif val1 != val2:
                diff[key] = ('changed', (val1, val2))
            else:
                diff[key] = ('unchanged', val1)
    return diff

def format_diff(diff, depth=0):
    """Форматирование словаря diff в строку."""
    lines = []
    indent = '  ' * depth
    for key, value in diff.items():
        status = value[0]
        if status == 'added':
            lines.append(f"{indent}+ {key}: {value[1]}")
        elif status == 'removed':
            lines.append(f"{indent}- {key}: {value[1]}")
        elif status == 'unchanged':
            lines.append(f"{indent}  {key}: {value[1]}")
        elif status == 'changed':
            val1, val2 = value[1]
            lines.append(f"{indent}- {key}: {val1}")
            lines.append(f"{indent}+ {key}: {val2}")
        elif status == 'nested':
            nested_str = format_diff(value[1], depth + 1)
            lines.append(f"{indent}  {key}: {{\n{nested_str}\n{indent}  }}")
    return '\n'.join(lines)

def generate_diff(file_path1, file_path2):
    """Главная функция — возвращает diff двух файлов как строку."""
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)
    diff_dict = generate_diff_dict(data1, data2)
    return "{\n" + format_diff(diff_dict, 1) + "\n}"
































