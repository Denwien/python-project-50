INDENT = "  "
ADD = "+ "
DEL = "- "
UNCHANGED = "  "


def format_value(value, depth):
    """Форматирует значение для stylish."""
    if isinstance(value, dict):
        lines = []
        indent = INDENT * (depth + 1)
        for k, v in value.items():
            lines.append(f"{indent}{UNCHANGED}{k}: {format_value(v, depth + 1)}")
        closing_indent = INDENT * depth
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def make_stylish(diff, depth=0):
    """Рекурсивно строит stylish-формат для diff."""
    lines = []
    indent = INDENT * depth

    for item in diff:
        key = item["name"]
        action = item["action"]

        if action == "nested":
            children_str = make_stylish(item["children"], depth + 1)
            lines.append(f"{indent}{UNCHANGED}{key}: {children_str}")
        elif action == "added":
            lines.append(f"{indent}{ADD}{key}: {format_value(item['value'], depth + 1)}")
        elif action == "deleted":
            lines.append(f"{indent}{DEL}{key}: {format_value(item['old_value'], depth + 1)}")
        elif action == "modified":
            lines.append(f"{indent}{DEL}{key}: {format_value(item['old_value'], depth + 1)}")
            lines.append(f"{indent}{ADD}{key}: {format_value(item['new_value'], depth + 1)}")
        elif action == "unchanged":
            lines.append(f"{indent}{UNCHANGED}{key}: {format_value(item['value'], depth + 1)}")

    return "{\n" + "\n".join(lines) + f"\n{indent}}}"


def format_diff_stylish(diff):
    return make_stylish(diff)
