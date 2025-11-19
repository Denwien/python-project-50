INDENT = 4
SIGN_INDENT = 2

def format_value(value, depth):
    if isinstance(value, dict):
        lines = []
        indent = ' ' * ((depth + 1) * INDENT)
        for k, v in value.items():
            lines.append(f"{indent}{k}: {format_value(v, depth + 1)}")
        return "{\n" + "\n".join(lines) + f"\n{' ' * (depth * INDENT)}}}"
    elif value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    return str(value)

def format_diff_stylish(diff, depth=0):
    lines = []
    indent = ' ' * (depth * INDENT)
    for item in diff:
        name = item['name']
        action = item['action']

        if action == 'nested':
            children_str = format_diff_stylish(item['children'], depth + 1)
            lines.append(f"{indent}    {name}: {children_str}")
        elif action == 'added':
            val_str = format_value(item['value'], depth + 1)
            lines.append(f"{indent[:-SIGN_INDENT]}  + {name}: {val_str}")
        elif action == 'removed':
            val_str = format_value(item['old_value'], depth + 1)
            lines.append(f"{indent[:-SIGN_INDENT]}  - {name}: {val_str}")
        elif action == 'unchanged':
            val_str = format_value(item['value'], depth + 1)
            lines.append(f"{indent}    {name}: {val_str}")
        elif action == 'changed':
            old_val = format_value(item['old_value'], depth + 1)
            new_val = format_value(item['value'], depth + 1)
            lines.append(f"{indent[:-SIGN_INDENT]}  - {name}: {old_val}")
            lines.append(f"{indent[:-SIGN_INDENT]}  + {name}: {new_val}")

    return "{\n" + "\n".join(lines) + f"\n{indent}}}"
