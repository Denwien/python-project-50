def format_value(value, depth):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if not isinstance(value, dict):
        return str(value)

    indent = "  " * (depth + 1)
    lines = []
    for key, val in value.items():
        formatted_val = format_value(val, depth + 1)
        lines.append(f"{indent}{key}: {formatted_val}")
    closing_indent = "  " * depth
    return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"


def format_diff_stylish(diff, depth=0):
    lines = []
    indent = "  " * depth
    sign_indent = "  " * (depth)  # для + / - на текущем уровне

    for node in diff:
        name = node["name"]
        action = node["action"]

        if action == "nested":
            nested = format_diff_stylish(node["children"], depth + 1)
            lines.append(f"{indent}  {name}: {nested}")
        elif action == "unchanged":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}  {name}: {value}")
        elif action == "deleted":
            value = format_value(node["old_value"], depth + 1)
            lines.append(f"{sign_indent}- {name}: {value}")
        elif action == "added":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{sign_indent}+ {name}: {value}")
        elif action == "modified":
            old_value = format_value(node["old_value"], depth + 1)
            new_value = format_value(node["new_value"], depth + 1)
            lines.append(f"{sign_indent}- {name}: {old_value}")
            lines.append(f"{sign_indent}+ {name}: {new_value}")

    return "{\n" + "\n".join(lines) + f"\n{indent}}}"


def format_stylish(diff):
    return format_diff_stylish(diff)
