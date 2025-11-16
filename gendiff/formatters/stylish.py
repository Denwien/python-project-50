SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '


def format_value(value, spaces_count=2):
    """Форматирует значение с фиксированными отступами и скобками для словарей"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict):
        indent = SEPARATOR * (spaces_count + 4)
        lines = []
        for key, val in value.items():
            formatted_val = format_value(val, spaces_count + 4)
            lines.append(f"{indent}{NONE}{key}: {formatted_val}")
        inner = "\n".join(lines)
        end_indent = SEPARATOR * (spaces_count + 2)
        return f"{{\n{inner}\n{end_indent}}}"
    return str(value)


def make_stylish_diff(diff, spaces_count=2):
    """Рекурсивно форматирует diff в стиль с фиксированными скобками и отступами"""
    indent = SEPARATOR * spaces_count
    lines = []

    for item in diff:
        key = item['name']
        action = item['action']

        if action == "unchanged":
            value = format_value(item.get('value'), spaces_count)
            lines.append(f"{indent}{NONE}{key}: {value}")

        elif action == "modified":
            old_value = format_value(item.get('old_value'), spaces_count)
            new_value = format_value(item.get('new_value'), spaces_count)
            lines.append(f"{indent}{DEL}{key}: {old_value}")
            lines.append(f"{indent}{ADD}{key}: {new_value}")

        elif action == "deleted":
            old_value = format_value(item.get('old_value'), spaces_count)
            lines.append(f"{indent}{DEL}{key}: {old_value}")

        elif action == "added":
            new_value = format_value(item.get('value'), spaces_count)
            lines.append(f"{indent}{ADD}{key}: {new_value}")

        elif action == 'nested':
            children = make_stylish_diff(item.get('children'), spaces_count + 4)
            lines.append(f"{indent}{NONE}{key}: {children}")

    inner = "\n".join(lines)
    end_indent = SEPARATOR * (spaces_count - 2)
    return f"{{\n{inner}\n{end_indent}}}"


def format_diff_stylish(data):
    return make_stylish_diff(data)
