import json
import yaml
from pathlib import Path

def parse_file(file_path):
    """Парсинг JSON или YAML файлов."""
    path = Path(file_path)
    ext = path.suffix.lower()
    with path.open(encoding="utf-8") as f:
        if ext in ['.json']:
            return json.load(f)
        elif ext in ['.yml', '.yaml']:
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

def format_value(value):
    """Форматируем значение для stylish diff."""
    if isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    return value

def generate_stylish(diff_dict, depth=0):
    """Генерация stylish diff строки."""
    lines = []
    indent = '  ' * depth
    for key in sorted(diff_dict.keys()):
        value = diff_dict[key]
        if isinstance(value, dict) and 'status' not in value:
            # Вложенный объект
            nested = generate_stylish(value, depth + 2)
            lines.append(f"{indent}  {key}: {nested}")
        else:
            status = value.get('status')
            if status == 'added':
                lines.append(f"{indent}+ {key}: {format_value(value['value'])}")
            elif status == 'removed':
                lines.append(f"{indent}- {key}: {format_value(value['value'])}")
            elif status == 'unchanged':
                lines.append(f"{indent}  {key}: {format_value(value['value'])}")
            elif status == 'changed':
                lines.append(f"{indent}- {key}: {format_value(value['old_value'])}")
                lines.append(f"{indent}+ {key}: {format_value(value['new_value'])}")
    return "{\n" + '\n'.join(lines) + f"\n{indent}}}"

def build_diff(data1, data2):
    """Строим словарь с информацией об изменениях."""
    diff = {}
    keys = sorted(set(data1.keys()) | set(data2.keys()))
    for key in keys:
        if key not in data2:
            diff[key] = {'status': 'removed', 'value': data1[key]}
        elif key not in data1:
            diff[key] = {'status': 'added', 'value': data2[key]}
        elif isinstance(data1[key], dict) and isinstance(data2[key], dict):
            diff[key] = build_diff(data1[key], data2[key])
        elif data1[key] != data2[key]:
            diff[key] = {'status': 'changed', 'old_value': data1[key], 'new_value': data2[key]}
        else:
            diff[key] = {'status': 'unchanged', 'value': data1[key]}
    return diff

def generate_diff(file_path1, file_path2):
    """Основная функция для генерации diff."""
    data1 = parse_file(file_path1)
    data2 = parse_file(file_path2)
    diff_dict = build_diff(data1, data2)
    return generate_stylish(diff_dict)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: gendiff.py <file1> <file2>")
        sys.exit(1)
    diff = generate_diff(sys.argv[1], sys.argv[2])
    print(diff)










