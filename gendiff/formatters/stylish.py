# gendiff/formatters/stylish.py

INDENT = 4
SIGN_INDENT = 2


def format_value(value, depth):
    """Форматирование значения для stylish"""
    if isinstance(value, dict):
        lines = []
        indent = ' ' * (depth * INDENT)
        lines.append('{')
        for k, v in value.items():
            lines.append(f"{indent}{' ' * INDENT}{k}: {format_value(v, depth + 1)}")
        lines.append(f"{indent}}}")
        return '\n'.join(lines)
    elif value is True:
        return 'true'
    elif value is False:
        return 'false'
    elif value is None:
        return 'null'
    else:
        return str(value)


def format_diff_stylish(diff, depth=0):
    """Форматирование списка изменений в stylish"""
    lines = []
    indent = ' ' * (depth * INDENT)
    for item in diff:
        action = item['action']
        name = item['name']

        if action == 'nested':
            lines.append(f"{indent}    {name}: {{")
            lines.append(format_diff_stylish(item['children'], depth + 1))
            lines.append(f"{indent}    }}")
        elif action == 'added':
            lines.append(f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {name}: {format_value(item['value'], depth + 1)}")
        elif action == 'removed':
            lines.append(f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {name}: {format_value(item['value'], depth + 1)}")
        elif action == 'changed':
            lines.append(f"{indent}{' ' * (INDENT - SIGN_INDENT)}- {name}: {format_value(item['old_value'], depth + 1)}")
            lines.append(f"{indent}{' ' * (INDENT - SIGN_INDENT)}+ {name}: {format_value(item['new_value'], depth + 1)}")
        elif action == 'unchanged':
            lines.append(f"{indent}    {name}: {format_value(item['value'], depth + 1)}")
        else:
            raise ValueError(f"Unknown action: {action}")

    return '\n'.join(lines)


def format_diff(diff):
    """Обёртка для stylish, добавляем внешние фигурные скобки"""
    return '{\n' + format_diff_stylish(diff) + '\n}'
