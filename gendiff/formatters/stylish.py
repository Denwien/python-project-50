# gendiff/formatters/stylish.py

INDENT_SIZE = 4


def stringify(value, depth: int) -> str:
    """Преобразование значения в строку с учётом вложенности."""
    if isinstance(value, dict):
        lines = ['{']
        for key, inner_value in value.items():
            indent = ' ' * ((depth + 1) * INDENT_SIZE)
            lines.append(f'{indent}{key}: {stringify(inner_value, depth + 1)}')
        closing_indent = ' ' * (depth * INDENT_SIZE)
        lines.append(f'{closing_indent}}}')
        return '\n'.join(lines)

    if value is None:
        return 'null'

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def make_stylish(diff: list[dict], depth: int = 0) -> str:
    """Рекурсивное построение строки в формате stylish."""
    lines: list[str] = ['{']
    base_indent = ' ' * (depth * INDENT_SIZE)

    for node in diff:
        key = node['name']
        action = node['action']

        if action == 'nested':
            children_str = make_stylish(node['children'], depth + 1)
            lines.append(f'{base_indent}    {key}: {children_str}')
            continue

        if action == 'unchanged':
            value = stringify(node['value'], depth + 1)
            lines.append(f'{base_indent}    {key}: {value}')
            continue

        if action == 'added':
            # ВАЖНО: для added используется поле value, а не new_value
            value = stringify(node['value'], depth + 1)
            lines.append(f'{base_indent}  + {key}: {value}')
            continue

        if action == 'deleted':
            value = stringify(node['old_value'], depth + 1)
            lines.append(f'{base_indent}  - {key}: {value}')
            continue

        if action == 'modified':
            old_value = stringify(node['old_value'], depth + 1)
            new_value = stringify(node['new_value'], depth + 1)
            lines.append(f'{base_indent}  - {key}: {old_value}')
            lines.append(f'{base_indent}  + {key}: {new_value}')
            continue

        raise ValueError(f'Unknown action: {action!r}')

    closing_indent = ' ' * (depth * INDENT_SIZE)
    lines.append(f'{closing_indent}}}')
    return '\n'.join(lines)


def format_diff_stylish(diff: list[dict]) -> str:
    return make_stylish(diff)
