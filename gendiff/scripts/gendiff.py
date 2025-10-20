import yaml
import json
from pathlib import Path

def format_value(value):
    """Форматирование значения для diff."""
    if isinstance(value, bool):
        return str(value).lower()
    if value is None:
        return "null"
    return str(value)

def load_file(file_path):
    """Загружает YAML или JSON файл и возвращает словарь."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File {file_path} does not exist")
    if path.suffix in (".yml", ".yaml"):
        with open(path) as f:
            return yaml.safe_load(f) or {}
    elif path.suffix == ".json":
        with open(path) as f:
            return json.load(f) or {}
    else:
        raise ValueError("Unsupported file format. Only JSON and YAML are supported.")

def generate_diff(file_path1, file_path2):
    """Генерация diff между двумя файлами в формате stylish."""
    data1 = load_file(file_path1)
    data2 = load_file(file_path2)

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))
    diff_lines = []
    unchanged_block = []

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if val1 == val2:
            unchanged_block.append(f"{key}: {format_value(val1)}")
        else:
            # добавляем предыдущий блок неизменных ключей, если есть
            if unchanged_block:
                diff_lines.append("- " + unchanged_block[0])
                for line in unchanged_block[1:]:
                    diff_lines.append("  " + line)
                unchanged_block = []

            if key in data1 and key not in data2:
                diff_lines.append(f"- {key}: {format_value(val1)}")
            elif key not in data1 and key in data2:
                diff_lines.append(f"+ {key}: {format_value(val2)}")
            else:  # ключ есть в обоих, но значения разные
                diff_lines.append(f"- {key}: {format_value(val1)}")
                diff_lines.append(f"+ {key}: {format_value(val2)}")

    # добавляем оставшийся блок неизменных ключей
    if unchanged_block:
        diff_lines.append("- " + unchanged_block[0])
        for line in unchanged_block[1:]:
            diff_lines.append("  " + line)

    return "{\n  " + "\n  ".join(diff_lines) + "\n}"








