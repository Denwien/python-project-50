SEPARATOR = " "


def format_value(value, depth, offset=0):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if not isinstance(value, dict):
        return str(value) if value != "" else ""

    indent = SEPARATOR * (depth * 2 + 2 + offset)
    lines = []
    for key, val in value.items():
        formatted_val = format_value(val, depth + 1, offset)
        if formatted_val and formatted_val[0] == "\n":
            lines.append(f"{indent}{key}:{formatted_val}")
        elif formatted_val:
            lines.append(f"{indent}{key}: {formatted_val}")
        else:
            lines.append(f"{indent}{key}:")

    return "\n" + "\n".join(lines)


def make_stylish_diff(diff, depth=0):
    lines = []

    for item in diff:
        key = item["name"]
        action = item["action"]
        indent = SEPARATOR * (depth * 2)

        if action == "unchanged":
            value = item.get("value")
            formatted = format_value(value, depth)
            if isinstance(value, dict):
                lines.append(f"{indent}{key}:{formatted}")
            elif formatted:
                lines.append(f"{indent}{key}: {formatted}")
            else:
                lines.append(f"{indent}{key}:")

        elif action == "modified":
            old_value = item.get("old_value")
            new_value = item.get("new_value")
            old_formatted = format_value(old_value, depth, offset=2)
            new_formatted = format_value(new_value, depth, offset=2)

            old_line = (
                f"{indent}- {key}:{'' if isinstance(old_value, dict) else ' '}"
                f"{old_formatted}"
            )
            new_line = (
                f"{indent}+ {key}:{'' if isinstance(new_value, dict) else ' '}"
                f"{new_formatted}"
            )

            lines.append(old_line.rstrip())
            lines.append(new_line.rstrip())

        elif action == "deleted":
            old_value = item.get("old_value")
            formatted = format_value(old_value, depth)
            lines.append(
                f"{indent}- {key}:{'' if isinstance(old_value, dict) else ' '}"
                f"{formatted}".rstrip()
            )

        elif action == "added":
            value = item.get("value")
            formatted = format_value(value, depth)
            lines.append(
                f"{indent}+ {key}:{'' if isinstance(value, dict) else ' '}"
                f"{formatted}".rstrip()
            )

        elif action == "nested":
            children_diff = make_stylish_diff(item.get("children"), depth + 1)
            lines.append(f"{indent}{key}:\n{children_diff}")

    return "\n".join(lines)


def format_diff_stylish(data):
    return make_stylish_diff(data)
