INDENT_SIZE = 4


def stringify(value, depth):
    """Форматирование значений с учётом вложенности"""
    if isinstance(value, dict):
        lines = ['{']
        for key, inner_value in sorted(value.items()):
            indent = ' ' * ((depth + 1) * INDENT_SIZE)
            lines.append(f"{indent}{key}: {stringify(inner_value, depth + 1)}")
        closing_indent = ' ' * (depth * INDENT_SIZE)
        lines.append(f"{closing_indent}}}")
        return '\n'.join(lines)
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def make_stylish(diff, depth=0):
    """Основная функция форматирования diff в stylish формате"""
    lines = ['{']
    base_indent = ' ' * (depth * INDENT_SIZE)

    for node in diff:
        key = node['name']
        action = node['action']

        if action == 'nested':
            children = make_stylish(node['children'], depth + 1)
            lines.append(f"{base_indent}    {key}: {children}")
            continue

        if action == 'unchanged':
            value = stringify(node['value'], depth + 1)
            lines.append(f"{base_indent}    {key}: {value}")
            continue

        if action == 'added':
            value = stringify(node['value'], depth + 1)
            # ИСПРАВЛЕНИЕ: 2 пробела перед + вместо 4
            lines.append(f"{base_indent}  + {key}: {value}")
            continue

        if action == 'deleted':
            value = stringify(node['old_value'], depth + 1)
            # ИСПРАВЛЕНИЕ: 2 пробела перед - вместо 4
            lines.append(f"{base_indent}  - {key}: {value}")
            continue

        if action == 'modified':
            old_value = stringify(node['old_value'], depth + 1)
            new_value = stringify(node['new_value'], depth + 1)
            # ИСПРАВЛЕНИЕ: 2 пробела перед - и +
            lines.append(f"{base_indent}  - {key}: {old_value}")
            lines.append(f"{base_indent}  + {key}: {new_value}")
            continue

    closing_indent = ' ' * (depth * INDENT_SIZE)
    lines.append(f"{closing_indent}}}")
    return '\n'.join(lines)


def format_diff_stylish(diff):
    """Форматирование списка изменений в stylish формате"""
    return make_stylish(diff)
