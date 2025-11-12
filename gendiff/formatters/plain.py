def stringify(value):
    """Преобразует значение для plain-формата."""
    if isinstance(value, dict) or isinstance(value, list):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"
    if value is None:
        return 'null'
    if isinstance(value, bool):
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
            val = stringify(node['value'])
            lines.append(
                f"Property '{current_path}' was added with value: " 
                f"{val}"
            )

        elif action == 'deleted':
            lines.append(f"Property '{current_path}' was removed")

        elif action == 'modified':
            old_val = stringify(node['old_value'])
            new_val = stringify(node['new_value'])
            lines.append(
                f"Property '{current_path}' was updated. "
                f"From {old_val} to {new_val}"
            )

    for node in diff_tree:
        walk(node)

    return '\n'.join(lines)
