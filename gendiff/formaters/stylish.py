SEPARATOR = "  "
ADD = "+ "
DEL = "- "
NONE = "  "


def format_value(value, depth):
    """Форматирование значения с учётом отступов."""
    if isinstance(value, dict):
        lines = []
        indent = SEPARATOR * (depth + 1)
        for k, v in value.items():
            lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
        closing_indent = SEPARATOR * depth
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def make_stylish(diff, depth=0):
    lines = []
    indent = SEPARATOR * depth

    for node in diff:
        key = node["name"]
        action = node["action"]

        if action == "nested":
            children = make_stylish(node["children"], depth + 2)
            lines.append(f"{indent}  {key}: {{\n{children}\n{indent}  }}")
        elif action == "added":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}+ {key}: {value}")
        elif action == "deleted":
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}- {key}: {value}")
        else:  # unchanged
            value = format_value(node["value"], depth + 1)
            lines.append(f"{indent}  {key}: {value}")

    return "\n".join(lines)


def format_diff_stylish(diff):
    """Форматирование diff в стиль stylish для верхнего уровня."""
    return make_stylish(diff, depth=0)




























