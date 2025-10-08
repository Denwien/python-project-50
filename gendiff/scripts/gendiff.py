import json
from pathlib import Path
import yaml


def read_file(file_path):
    """Читает JSON или YAML файл и возвращает словарь."""
    file_path = Path(file_path)
    if file_path.suffix in (".json",):
        with open(file_path, encoding="utf-8") as f:
            return json.load(f)
    elif file_path.suffix in (".yml", ".yaml"):
        with open(file_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported file format: {file_path.suffix}")


def format_value(value):
    """Форматирует значение для вывода в diff."""
    if isinstance(value, bool):
        return "true" if value else "false"
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        return "[complex value]"
    return str(value)


def build_diff(d1, d2, indent=2):
    """Рекурсивно строит diff между двумя словарями."""
    keys = sorted(set(d1.keys()) | set(d2.keys()))
    lines = []

    for key in keys:
        if key not in d1:
            lines.append(f"{' ' * indent}+ {key}: {format_value(d2[key])}")
        elif key not in d2:
            lines.append(f"{' ' * indent}- {key}: {format_value(d1[key])}")
        else:
            val1, val2 = d1[key], d2[key]
            if isinstance(val1, dict) and isinstance(val2, dict):
                nested = build_diff(val1, val2, indent + 4)
                lines.append(f"{' ' * indent}  {key}: {{\n{nested}\n{' ' * indent}  }}")
            elif val1 != val2:
                lines.append(f"{' ' * indent}- {key}: {format_value(val1)}")
                lines.append(f"{' ' * indent}+ {key}: {format_value(val2)}")
            else:
                lines.append(f"{' ' * indent}  {key}: {format_value(val1)}")

    return "\n".join(lines)


def generate_diff(file_path1, file_path2):
    """Главная функция: генерирует diff двух файлов."""
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)
    diff = build_diff(data1, data2)
    return "{\n" + diff + "\n}"































