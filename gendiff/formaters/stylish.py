SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '


def format_value(value, depth):
    """Форматирование значения с учётом отступов."""
    if isinstance(value, dict):
        lines = []
        indent = SEPARATOR * (depth + 2)
        closing_indent = SEPARATOR * depth
        for k, v in value.items():
            lines.append(f"{indent}{k}: {format_value(v, depth + 2)}")
        return "{\n" + "\n".join(lines) + f"\n{closing_indent}}}"
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def make_stylish(diff, depth=0):
    """Рекурсивное форматирование списка изменений в стиле stylish."""
    lines = []
    indent = SEPARATOR * depth
    for node in diff:
        key = node["name"]
        action = node["action"]

        if action == "nested":
            children = make_stylish(node["children"], depth + 2)
            lines.append(f"{indent}{NONE}{key}: {{\n{children}\n{indent}{NONE}}}")
        elif action == "added":
            value = format_value(node["value"], depth + 2)
            lines.append(f"{indent}{ADD}{key}: {value}")
        elif action == "deleted":
            value = format_value(node["value"], depth + 2)
            lines.append(f"{indent}{DEL}{key}: {value}")
        elif action == "unchanged":
            value = format_value(node["value"], depth + 2)
            lines.append(f"{indent}{NONE}{key}: {value}")
        elif action == "modified":
            old_value = format_value(node["old_value"], depth + 2)
            new_value = format_value(node["new_value"], depth + 2)
            lines.append(f"{indent}{DEL}{key}: {old_value}")
            lines.append(f"{indent}{ADD}{key}: {new_value}")
    return "\n".join(lines)


def format_diff_stylish(diff):
    """Форматирование diff в стиль stylish для верхнего уровня."""
    return make_stylish(diff)























