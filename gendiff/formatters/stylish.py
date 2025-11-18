INDENT = "  "
PREFIX_ADDED = "+ "
PREFIX_REMOVED = "- "
PREFIX_UNCHANGED = "  "


def format_value(value, depth):
    if value is None:
        return "none"
    if isinstance(value, bool):
        return "true" if value else "false"
    if not isinstance(value, dict):
        return str(value)

    lines = []
    current_indent = INDENT * (depth + 1)
    for key, val in value.items():
        formatted_val = format_value(val, depth + 1)
        lines.append(f"{current_indent}{key}: {formatted_val}")
    closing_indent = INDENT * depth
    return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"


def format_diff_stylish(diff, depth=0):
    lines = []
    indent = INDENT * depth
    sign_indent = INDENT * depth  # для + / - на текущем уровне

    for node in diff:
        name = node["name"]
        action = node["action"]

        if action == "nested":
            nested = format_diff_stylish(node["children"], depth + 1)
            lines.append(f"{indent}{PREFIX_UNCHANGED}{name}: {nested}")
        elif action == "unchanged":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}{PREFIX_UNCHANGED}{name}: {value}")
        elif action == "deleted":
            value = format_value(node["old_value"], depth + 1)
            lines.append(f"{sign_indent}{PREFIX_REMOVED}{name}: {value}")
        elif action == "added":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{sign_indent}{PREFIX_ADDED}{name}: {value}")
        elif action == "modified":
            old_value = format_value(node["old_value"], depth + 1)
            new_value = format_value(node["new_value"], depth + 1)
            lines.append(f"{sign_indent}{PREFIX_REMOVED}{name}: {old_value}")
            lines.append(f"{sign_indent}{PREFIX_ADDED}{name}: {new_value}")

    return "\n".join(lines)  # убрали внешние {}


def format_stylish(diff):
    return format_diff_stylish(diff)