import json
import yaml
from pathlib import Path


def read_file(file_path):
    ext = Path(file_path).suffix.lower()
    with open(file_path, 'r', encoding='utf-8') as f:
        if ext == ".json":
            return json.load(f)
        elif ext in (".yml", ".yaml"):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {ext}")


def build_diff(data1, data2):
    diff_lines = []

    all_keys = sorted(set(data1) | set(data2))
    for key in all_keys:
        if key not in data1:
            diff_lines.append(f"  + {key}: {data2[key]}")
        elif key not in data2:
            diff_lines.append(f"  - {key}: {data1[key]}")
        elif data1[key] != data2[key]:
            diff_lines.append(f"  - {key}: {data1[key]}")
            diff_lines.append(f"  + {key}: {data2[key]}")
        else:
            diff_lines.append(f"    {key}: {data1[key]}")

    return "{\n" + "\n".join(diff_lines) + "\n}"


def generate_diff(file_path1, file_path2):
    data1 = read_file(file_path1)
    data2 = read_file(file_path2)
    return build_diff(data1, data2)






























