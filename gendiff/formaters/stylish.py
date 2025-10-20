SEPARATOR = '  '
ADD = '+ '
DEL = '- '
UNCHANGED = '  '

def format_value(value, depth):
    if isinstance(value, dict):
        lines = []
        for k in sorted(value):
            lines.append(f"{'    ' * (depth + 1)}{k}: {format_value(value[k], depth + 1)}")
        return '\n'.join(lines)
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def make_stylish(diff, depth=0):
    lines = []
    indent = '' if depth == 0 else SEPARATOR * depth
    for node in diff:
        key = node['name']
        action = node['action']
        if action == 'nested':
            lines.append(f"{indent}{UNCHANGED}{key}:")
            lines.extend(make_stylish(node['children'], depth + 1))
        elif action == 'added':
            value = format_value(node['value'], depth)
            lines.append(f"{indent}{ADD}{key}: {value}")
        elif action == 'deleted':
            value = format_value(node['value'], depth)
            lines.append(f"{indent}{DEL}{key}: {value}")
        else:  # unchanged
            value = format_value(node['value'], depth)
            lines.append(f"{indent}{UNCHANGED}{key}: {value}")
    return lines

def format_diff_stylish(diff):
    return '\n'.join(make_stylish(diff))
