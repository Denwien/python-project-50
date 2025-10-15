import json
import sys

def build_diff(dict1, dict2):
    """Построение разницы между двумя словарями"""
    keys = sorted(set(dict1.keys()) | set(dict2.keys()))
    diff = {}
    for key in keys:
        if key not in dict1:
            diff[key] = {'status': 'added', 'value': dict2[key]}
        elif key not in dict2:
            diff[key] = {'status': 'removed', 'value': dict1[key]}
        elif isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            diff[key] = {'status': 'nested', 'children': build_diff(dict1[key], dict2[key])}
        elif dict1[key] != dict2[key]:
            diff[key] = {'status': 'changed', 'old_value': dict1[key], 'new_value': dict2[key]}
        else:
            diff[key] = {'status': 'unchanged', 'value': dict1[key]}
    return diff

def format_dict(val, indent):
    """Рекурсивное форматирование обычного словаря в YAML"""
    lines = []
    prefix = '  ' * indent
    for k, v in val.items():
        if isinstance(v, dict):
            lines.append(f"{prefix}{k}:")
            lines.extend(format_dict(v, indent + 1))
        else:
            val_str = "true" if v is True else "false" if v is False else "null" if v is None else str(v)
            lines.append(f"{prefix}{k}: {val_str}")
    return lines

def format_yaml(diff, indent=0):
    """Форматирование diff в YAML с правильными bool, null и отступами"""
    lines = []
    for key, info in diff.items():
        status = info['status']
        prefix = '  ' * indent

        if status == 'nested':
            lines.append(f"{prefix}{key}:")
            lines.extend(format_yaml(info['children'], indent + 1))
        elif status == 'added':
            val = info['value']
            if isinstance(val, dict):
                lines.append(f"{prefix}+ {key}:")
                lines.extend(format_dict(val, indent + 1))
            else:
                val_str = "true" if val is True else "false" if val is False else "null" if val is None else str(val)
                lines.append(f"{prefix}+ {key}: {val_str}")
        elif status == 'removed':
            val = info['value']
            if isinstance(val, dict):
                lines.append(f"{prefix}- {key}:")
                lines.extend(format_dict(val, indent + 1))
            else:
                val_str = "true" if val is True else "false" if val is False else "null" if val is None else str(val)
                lines.append(f"{prefix}- {key}: {val_str}")
        elif status == 'changed':
            old_val = info['old_value']
            new_val = info['new_value']

            if isinstance(old_val, dict):
                lines.append(f"{prefix}- {key}:")
                lines.extend(format_dict(old_val, indent + 1))
            else:
                val_str = "true" if old_val is True else "false" if old_val is False else "null" if old_val is None else str(old_val)
                lines.append(f"{prefix}- {key}: {val_str}")

            if isinstance(new_val, dict):
                lines.append(f"{prefix}+ {key}:")
                lines.extend(format_dict(new_val, indent + 1))
            else:
                val_str = "true" if new_val is True else "false" if new_val is False else "null" if new_val is None else str(new_val)
                lines.append(f"{prefix}+ {key}: {val_str}")
        else:  # unchanged
            val = info['value']
            if isinstance(val, dict):
                lines.append(f"{prefix}{key}:")
                lines.extend(format_dict(val, indent + 1))
            else:
                val_str = "true" if val is True else "false" if val is False else "null" if val is None else str(val)
                lines.append(f"{prefix}{key}: {val_str}")
    return lines

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python gendiff.py file1.json file2.json output.yaml")
        sys.exit(1)

    file1_path, file2_path, output_path = sys.argv[1], sys.argv[2], sys.argv[3]

    with open(file1_path) as f1, open(file2_path) as f2:
        dict1 = json.load(f1)
        dict2 = json.load(f2)

    diff = build_diff(dict1, dict2)
    yaml_lines = format_yaml(diff)

    with open(output_path, "w") as f:
        f.write("\n".join(yaml_lines) + "\n")




