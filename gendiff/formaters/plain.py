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
    result_lines = []

    for item in diff:
        name = item['name']
        action = item['action']
        path = f"{parent}.{name}" if parent else name

        if action == 'added':
            result_lines.append(
                f"Property '{path}' was added with value: {format_value_plain(item['value'])}"
            )
        elif action == 'deleted':
            result_lines.append(f"Property '{path}' was removed")
        elif action == 'changed':
            old_val = format_value_plain(item['old_value'])
            new_val = format_value_plain(item['new_value'])
            result_lines.append(
                f"Property '{path}' was updated. From {old_val} to {new_val}"
            )
        elif action == 'nested':
            result_lines.append(format_diff_plain(item['children'], path))

    return "\n".join(result_lines)
