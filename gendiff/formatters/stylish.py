INDENT_STEP = 4


def make_indent(depth, shift=0):
    return " " * (depth * INDENT_STEP - shift)


def format_value(value, depth):
    """Форматирует значение (в т.ч. вложенные словари)."""
    if not isinstance(value, dict):
        if value is True:
            return "true"
        if value is False:
            return "false"
        if value is None:
            return "null"
        return str(value)

    lines = ["{"]
    for key, val in value.items():
        lines.append(
            f"{make_indent(depth + 1)}{key}: {format_value(val, depth + 1)}"
        )
    lines.append(f"{make_indent(depth)}}}")
    return "\n".join(lines)


def make_stylish(diff, depth=1):
    """Рекурсивная генерация stylish-формата."""
    lines = ["{"]

    for key in sorted(diff.keys()):
        node = diff[key]
        action = node["action"]

        if action == "unchanged":
            lines.append(
                f"{make_indent(depth)}  {key}: "
                f"{format_value(node['value'], depth)}"
            )

        elif action == "added":
            lines.append(
                f"{make_indent(depth)}+ {key}: "
                f"{format_value(node['value'], depth)}"
            )

        elif action == "deleted":
            lines.append(
                f"{make_indent(depth)}- {key}: "
                f"{format_value(node['old_value'], depth)}"
            )

        elif action == "modified":
            lines.append(
                f"{make_indent(depth)}- {key}: "
                f"{format_value(node['old_value'], depth)}"
            )
            lines.append(
                f"{make_indent(depth)}+ {key}: "
                f"{format_value(node['new_value'], depth)}"
            )

        elif action == "nested":
            children = make_stylish(node["children"], depth + 1)
            lines.append(f"{make_indent(depth)}  {key}: {children}")

    lines.append(f"{make_indent(depth - 1)}}}")
    return "\n".join(lines)


def format_diff_stylish(diff):
    return make_stylish(diff)
