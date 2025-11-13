SEPARATOR = " "

def format_value(value, depth):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if not isinstance(value, dict):
        return str(value)
    indent = SEPARATOR * (depth * 4)
    lines = []
    for k, v in value.items():
        lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
    return "{\n" + "\n".join(lines) + f"\n{indent}}}"

def make_stylish_diff(diff, depth=0):
    lines = []
    indent = SEPARATOR * (depth * 4 - 2) if depth > 0 else ""
    for item in diff:
        key = item["name"]
        action = item["action"]

        if action == "nested":
            children = make_stylish_diff(item["children"], depth + 1)
            lines.append(f"{indent}  {key}: {children}")
        elif action == "unchanged":
            value = format_value(item["value"], depth + 1)
            lines.append(f"{indent}  {key}: {value}")
        elif action == "added":
            value = format_value(item["value"], depth + 1)
            lines.append(f"{indent}+ {key}: {value}")
        elif action == "deleted":
            value = format_value(item["old_value"], depth + 1)
            lines.append(f"{indent}- {key}: {value}")
        elif action == "modified":
            old_value = format_value(item["old_value"], depth + 1)
            new_value = format_value(item["new_value"], depth + 1)
            lines.append(f"{indent}- {key}: {old_value}")
            lines.append(f"{indent}+ {key}: {new_value}")

    return "\n".join(lines)

def format_diff_stylish(diff):
    return "{\n" + make_stylish_diff(diff) + "\n}"

