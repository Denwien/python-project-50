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
        lines.append(f"{indent}    {k}: {format_value(v, depth + 1)}")
    return "{\n" + "\n".join(lines) + f"\n{indent}}}"


def make_stylish(diff, depth=0):
    lines = []
    indent = SEPARATOR * (depth * 4)

    for node in diff:
        name = node["name"]
        action = node["action"]

        if action == "nested":
            children = make_stylish(node["children"], depth + 1)
            lines.append(f"{indent}    {name}: {{\n{children}\n{indent}    }}")
        elif action == "unchanged":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}    {name}: {value}")
        elif action == "added":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}  + {name}: {value}")
        elif action == "deleted":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}  - {name}: {value}")
        elif action == "modified":
            old_value = format_value(node["old_value"], depth + 1)
            new_value = format_value(node["new_value"], depth + 1)
            lines.append(f"{indent}  - {name}: {old_value}")
            lines.append(f"{indent}  + {name}: {new_value}")

    return "\n".join(lines)


def format_diff_stylish(diff):
    return "{\n" + make_stylish(diff) + "\n}"
