INDENT = 4
SIGN_INDENT = 2


def to_str(value, depth):
    """Конвертирует значение в строку для stylish формата."""
    if isinstance(value, dict):
        lines = []
        indent = ' ' * (depth * INDENT)
        for k, v in value.items():
            lines.append(f"{indent}{k}: {to_str(v, depth + 1)}")
        return "{\n" + "\n".join(lines) + f"\n{indent[:-INDENT]}}}"
    elif value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    else:
        return str(value)


def format_stylish(diff, depth=0):
    """Рекурсивно форматирует diff для stylish."""
    lines = []
    indent = ' ' * (depth * INDENT)
    for item in diff:
        key = item['key']
        status = item['status']
        if status == 'nested':
            lines.append(f"{indent}{key}: {format_stylish(item['children'], depth + 1)}")
        elif status == 'added':
            lines.append(f"{indent[:-SIGN_INDENT]}+ {key}: {to_str(item['value'], depth + 1)}")
        elif status == 'removed':
            lines.append(f"{indent[:-SIGN_INDENT]}- {key}: {to_str(item['value'], depth + 1)}")
        elif status == 'unchanged':
            lines.append(f"{indent}{key}: {to_str(item['value'], depth + 1)}")
        elif status == 'changed':
            lines.append(f"{indent[:-SIGN_INDENT]}- {key}: {to_str(item['old_value'], depth + 1)}")
            lines.append(f"{indent[:-SIGN_INDENT]}+ {key}: {to_str(item['new_value'], depth + 1)}")
    return "{\n" + "\n".join(lines) + f"\n{indent}}}"
