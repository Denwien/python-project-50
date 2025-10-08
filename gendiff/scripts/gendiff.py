import json
import yaml
from pathlib import Path
from typing import Any


def read_file(file_path: str) -> dict[str, Any]:
    """Читает JSON или YAML файл и возвращает как словарь."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix in (".yml", ".yaml"):
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f)
    elif path.suffix == ".json":
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")


def generate_diff(file_path1: str, file_path2: str) -> str:
    """Генерирует diff между двумя JSON/YAML файлами в формате строки."""
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)

    diff_lines = ["{"]

    all_keys = sorted(set(data1.keys()) | set(data2.keys()))

    for key in all_keys:
        val1 = data1.get(key)
        val2 = data2.get(key)

        if key in data1 and key not in data2:
            diff_lines.append(f"  - {key}: {val1}")
        elif key not in data1 and key in data2:
            diff_lines.append(f"  + {key}: {val2}")
        elif val1 != val2:
            diff_lines.append(f"  - {key}: {val1}")
            diff_lines.append(f"  + {key}: {val2}")
        else:
            diff_lines.append(f"    {key}: {val1}")

    diff_lines.append("}")
    return "\n".join(diff_lines)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: gendiff <file1> <file2>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    result = generate_diff(file1, file2)
    print(result)











