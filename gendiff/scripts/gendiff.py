import json
import yaml
from pathlib import Path

def parse_file(file_path):
    ext = Path(file_path).suffix.lower()
    with open(file_path, 'r', encoding='utf-8') as f:
        if ext == '.json':
            return json.load(f)
        elif ext in {'.yml', '.yaml'}:
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

def to_str(value, depth):
    indent = '    ' * depth
    if isinstance(value, dict):
        lines = ['{']
        for k in sorted(value.keys()):
            lines.append(f"{indent}    {k}: {to_str(value[k], depth + 1)}")
        lines.append(f"{indent}}}")
        return '\n'.join(lines)
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)

def build_diff(d1, d2, depth=0):
    lines = []
    indent = '    ' * depth
    keys = sorted(d1.keys() | d2.keys())
    
    for key in keys:
        if key not in d1:
            lines.append(f"{indent}  + {key}: {to_str(d2[key], depth + 1)}")
        elif key not in d2:
            lines.append(f"{indent}  - {key}: {to_str(d1[key], depth + 1)}")
        elif isinstance(d1[key], dict) and isinstance(d2[key], dict):
            nested = build_diff(d1[key], d2[key], depth + 1)
            lines.append(f"{indent}    {key}: {{\n{nested}\n{indent}    }}")
        elif d1[key] != d2[key]:
            lines.append(f"{indent}  - {key}: {to_str(d1[key], depth + 1)}")
            lines.append(f"{indent}  + {key}: {to_str(d2[key], depth + 1)}")
        else:
            lines.append(f"{indent}    {key}: {to_str(d1[key], depth + 1)}")
    return '\n'.join(lines)

def generate_diff(file1, file2):
    data1 = parse_file(file1)
    data2 = parse_file(file2)
    return '{\n' + build_diff(data1, data2) + '\n}'





























