import json
from pathlib import Path
import yaml

# Настройка представления булевых значений для YAML
def bool_representer(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:bool', str(data).lower())

yaml.add_representer(bool, bool_representer)

def read_file(file_path: str):
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"No such file: '{file_path}'")

    ext = path.suffix.lower()
    content = path.read_text(encoding='utf-8')
    if ext == '.json':
        return json.loads(content)
    elif ext in ('.yml', '.yaml'):
        return yaml.safe_load(content)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def generate_diff(file_path1: str, file_path2: str) -> str:
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)
    return dict_diff(data1, data2)

def dict_diff(d1, d2, level=0):
    """Рекурсивное сравнение словарей и формирование строки diff."""
    diff_lines = []
    indent = "  " * level

    all_keys = sorted(d1.keys() | d2.keys())
    for key in all_keys:
        val1 = d1.get(key, None)
        val2 = d2.get(key, None)

        if key not in d1:
            diff_lines.append(f"{indent}+ {key}: {format_value(val2, level + 1)}")
        elif key not in d2:
            diff_lines.append(f"{indent}- {key}: {format_value(val1, level + 1)}")
        elif isinstance(val1, dict) and isinstance(val2, dict):
            nested = dict_diff(val1, val2, level + 1)
            diff_lines.append(f"{indent}  {key}: {{\n{nested}\n{indent}  }}")
        elif val1 != val2:
            diff_lines.append(f"{indent}- {key}: {format_value(val1, level + 1)}")
            diff_lines.append(f"{indent}+ {key}: {format_value(val2, level + 1)}")
        else:
            diff_lines.append(f"{indent}  {key}: {format_value(val1, level + 1)}")

    return "\n".join(diff_lines)

def format_value(value, level):
    """Форматирование значения для вывода в diff."""
    indent = "  " * level
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            lines.append(f"{indent}  {k}: {format_value(v, level + 1)}")
        return "{\n" + "\n".join(lines) + f"\n{indent}}}"
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return str(value)



































