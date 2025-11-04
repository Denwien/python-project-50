def format_diff_plain(diff, path=''):
    lines = []

    for item in diff:
        name = item['name']
        action = item['action']
        property_path = f"{path}.{name}" if path else name

        if action == 'nested':
            lines.extend(format_diff_plain(item['children'], property_path))
        elif action == 'added':
            value = stringify(item['value'])
            lines.append(f"Property '{property_path}' was added with value: {value}")
        elif action == 'deleted':
            lines.append(f"Property '{property_path}' was removed")
        elif action == 'changed':
            old = stringify(item['old_value'])
            new = stringify(item['new_value'])
            lines.append(f"Property '{property_path}' was updated. From {old} to {new}")

    return '\n'.join(lines)


def stringify(value):
    if isinstance(value, dict):
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    elif isinstance(value, str):
        return f"'{value}'"
    return str(value)
