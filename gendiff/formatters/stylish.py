SEPARATOR = " "

def format_value(value, depth):
    indent = " " * (depth * 4)
    bracket_indent = " " * ((depth - 1) * 4)

    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if not isinstance(value, dict):
        return str(value)

    lines = ["{"]

    for key, val in value.items():
        lines.append(f"{indent}{key}: {format_value(val, depth + 1)}")

    lines.append(f"{bracket_indent}}}")
    return "\n".join(lines)


def make_stylish_diff(diff, depth=0):
    indent = " " * (depth * 4)
    sign_indent = " " * (depth * 4 - 2) if depth > 0 else ""

    lines = ["{"]

    for item in diff:
        key = item["name"]
        action = item["action"]

        if action == "nested":
            children = make_stylish_diff(item["children"], depth + 1)
            lines.append(f"{indent}    {key}: {children}")
            continue

        if action == "unchanged":
            value = format_value(item["value"], depth + 1)
            lines.append(f"{indent}    {key}: {value}")
            continue

        if action == "added":
            value = format_value(item["value"], depth + 1)
            lines.append(f"{sign_indent}+ {key}: {value}")
            continue

        if action == "deleted":
            value = format_value(item["old_value"], depth + 1)
            lines.append(f"{sign_indent}- {key}: {value}")
            continue

        if action == "modified":
            old = format_value(item["old_value"], depth + 1)
            new = format_value(item["new_value"], depth + 1)
            lines.append(f"{sign_indent}- {key}: {old}")
            lines.append(f"{sign_indent}+ {key}: {new}")
            continue

    lines.append(f"{indent}}}")
    return "\n".join(lines)

def format_diff_stylish(data):
    return make_stylish_diff(data)