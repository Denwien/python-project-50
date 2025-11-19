INDENT_SIZE = 2
PREFIX_ADDED = "+ "
PREFIX_REMOVED = "- "
PREFIX_UNCHANGED = "  "


def format_value(value, depth):
    """Форматирует значение с учетом глубины вложенности."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if not isinstance(value, dict):
        return str(value)

    indent = " " * (depth * INDENT_SIZE)
    lines = []
    for k, v in value.items():
        formatted_v = format_value(v, depth + 1)
        if isinstance(v, dict):
            lines.append(f"{indent}{k}: {formatted_v}")
        else:
            lines.append(f"{indent}{k}: {formatted_v}")
    return "\n" + "\n".join(lines)


def make_stylish_diff(diff, depth=0):
    lines = []
    indent = " " * (depth * INDENT_SIZE)

    for item in diff:
        key = item["name"]
        action = item["action"]

        if action == "nested":
            children = make_stylish_diff(item["children"], depth + 1)
            lines.append(f"{indent}{key}:\n{children}")
        elif action == "added":
            formatted = format_value(item["value"], depth + 1)
            lines.append(f"{indent}{PREFIX_ADDED}{key}: {formatted}".rstrip())
        elif action == "deleted":
            formatted = format_value(item["old_value"], depth + 1)
            lines.append(f"{indent}{PREFIX_REMOVED}{key}: {formatted}".rstrip())
        elif action == "modified":
            old_formatted = format_value(item["old_value"], depth + 1)
            new_formatted = format_value(item["new_value"], depth + 1)
            lines.append(f"{indent}{PREFIX_REMOVED}{key}: {old_formatted}".rstrip())
            lines.append(f"{indent}{PREFIX_ADDED}{key}: {new_formatted}".rstrip())
        elif action == "unchanged":
            formatted = format_value(item["value"], depth + 1)
            lines.append(f"{indent}{PREFIX_UNCHANGED}{key}: {formatted}".rstrip())

    return "\n".join(lines)


def format_diff_stylish(data):
    return make_stylish_diff(data)
