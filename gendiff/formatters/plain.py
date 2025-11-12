def stringify(value):
    if isinstance(value, dict) or isinstance(value, list):
        return '[complex value]'
    elif isinstance(value, str):
        return f"'{value}'"
    elif value is None:
        return 'null'
    elif isinstance(value, bool):
        return str(value).lower()
    return str(value)


def format_plain(diff_tree):
    """
    Форматирует дерево изменений в plain.
    """
    lines = []

    def walk(node, path=''):
        name = node.get('name')
        current_path = f"{path}.{name}" if path else name
        action = node.get('action')

        if action == 'nested':
            for child in node['children']:
                walk(child, current_path)
        elif action == 'added':
            lines.append(
                f"Property '{current_path}' was added with value: "
                f"{stringify(node['value'])}"
            )
        elif action == 'deleted':
            lines.append(f"Property '{current_path}' was removed")
        elif action == 'modified':
            lines.append(
                f"Property '{current_path}' was updated. "
                f"From {stringify(node['old_value'])} to {stringify(node['new_value'])}"
            )

    for node in diff_tree:
        walk(node)

    return '\n'.join(lines)
