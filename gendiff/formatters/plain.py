def format_value_plain(value):
    if isinstance(value, dict):
        return '[complex value]'
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def format_diff_plain(diff, path=''):
    lines = []

    for item in diff:
        name = item['name']
        action = item['action']
        property_path = f"{path}.{name}" if path else name

        if action == 'nested':
            lines.extend(format_diff_plain(item['children'], property_path))
        elif action == 'added':
            value = format_value_plain(item.get('value'))
            lines.append(f"Property '{property_path}' was added with value: {value}")
        elif action == 'deleted':
            lines.append(f"Property '{property_path}' was removed")
        elif action == 'changed':
            old_val = format_value_plain(item.get('old_value'))
            new_val = format_value_plain(item.get('new_value'))
            lines.append(f"Property '{property_path}' was updated. From {old_val} to {new_val}")

    return '\n'.join(lines)
