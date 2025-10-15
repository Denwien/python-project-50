def format_value(value, depth):
    """Преобразует значение в строку с правильными отступами для stylish."""
    indent = '  ' * depth
    if isinstance(value, dict):
        lines = []
        for k in sorted(value.keys()):
            lines.append(f"{indent}  {k}: {format_value(value[k], depth + 1)}")
        return '{\n' + '\n'.join(lines) + f'\n{indent}}}'
    elif isinstance(value, bool):
        return str(value).lower()
    elif value is None:
        return 'null'
    else:
        return str(value)

def make_stylish_diff(diff, depth=0):
    lines = []
    indent = '  ' * depth
    for item in diff:
        key = item['name']
        action = item['action']
        if action == 'nested':
            children = make_stylish_diff(item['children'], depth + 1)
            lines.append(f"{indent}  {key}: {children}")
        elif action == 'added':
            value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}+ {key}: {value}")
        elif action == 'deleted':
            value = format_value(item['old_value'], depth + 1)
            lines.append(f"{indent}- {key}: {value}")
        elif action == 'modified':
            old_value = format_value(item['old_value'], depth + 1)
            new_value = format_value(item['new_value'], depth + 1)
            lines.append(f"{indent}- {key}: {old_value}")
            lines.append(f"{indent}+ {key}: {new_value}")
        else:  # unchanged
            value = format_value(item['value'], depth + 1)
            lines.append(f"{indent}  {key}: {value}")
    return '{\n' + '\n'.join(lines) + f'\n{indent}}}'

def format_stylish(diff):
    """Главная функция для генерации stylish diff без внешнего обрамления."""
    return make_stylish_diff(diff, depth=0)
