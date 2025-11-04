def format_value_plain(value):
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def format_diff_plain(diff, parent=''):
    lines = []
    for item in diff:
        name = item['name']
        full_path = f"{parent}.{name}" if parent else name
        action = item['action']

        if action == 'added':
            value = format_value_plain(item['value'])
            lines.append(f"Property '{full_path}' was added with value: {value}")
        elif action == 'deleted':
            lines.append(f"Property '{full_path}' was removed")
        elif action == 'changed':
            old_val = format_value_plain(item['old_value'])
            new_val = format_value_plain(item['new_value'])
            lines.append(f"Property '{full_path}' was updated. From {old_val} to {new_val}")
        elif action == 'nested':
            lines.extend(format_diff_plain(item['children'], full_path))
    return '\n'.join(lines)
