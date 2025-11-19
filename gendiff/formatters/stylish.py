INDENT = 4
SIGN_INDENT = 2  # для "+ " и "- "

def format_value(value, depth):
    """Форматирование значения с учётом вложенности."""
    if isinstance(value, dict):
        lines = []
        indent = ' ' * (depth * INDENT)
        for k, v in value.items():
            lines.append(f"{indent}    {k}: {format_value(v, depth + 1)}")
        return "{\n" + "\n".join(lines) + f"\n{indent}}}"
    elif value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    else:
        return str(value)

def format_diff_stylish(diff, depth=0):
    """Форматирование diff в стиль 'stylish'."""
    lines = []
    indent = ' ' * (depth * INDENT)
    for item in diff:
        name = item['name']
        action = item['action']

        if action == 'nested':
            children_str = format_diff_stylish(item['children'], depth + 1)
            lines.append(f"{indent}    {name}: {children_str}")
        elif action == 'added':
            value_str = format_value(item['value'], depth + 1)
            lines.append(f"{indent[:-SIGN_INDENT]}  + {name}: {value_str}")
        elif action == 'removed':
            value_str = format_value(item['old_value'], depth + 1)
            lines.append(f"{indent[:-SIGN_INDENT]}  - {name}: {value_str}")
        elif action == 'unchanged':
            value_str = format_value(item['value'], depth + 1)
            lines.append(f"{indent}    {name}: {value_str}")

    return "{\n" + "\n".join(lines) + f"\n{indent}}}"
