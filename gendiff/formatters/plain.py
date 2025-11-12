def format_plain(diff_tree):
    """
    Форматирует дерево изменений в plain.
    """

    def stringify(value):
        if isinstance(value, (dict, list)):
            return "[complex value]"
        if isinstance(value, str):
            return f"'{value}'"
        if value is None:
            return "null"
        if isinstance(value, bool):
            return str(value).lower()
        return str(value)

    lines = []

    def walk(node, path=""):
        name = node.get("name")
        current_path = f"{path}.{name}" if path else name
        action = node.get("action")

        if action == "nested":
            for child in node["children"]:
                walk(child, current_path)

        elif action == "added":
            value_str = stringify(node["value"])
            lines.append(
                f"Property '{current_path}' was added with value: {value_str}"
            )

        elif action == "deleted":
            lines.append(f"Property '{current_path}' was removed")

        elif action == "modified":
            old_str = stringify(node["old_value"])
            new_str = stringify(node["new_value"])
            lines.append(
                f"Property '{current_path}' was updated. "
                f"From {old_str} to {new_str}"
            )

    for node in diff_tree:
        walk(node)

    return "\n".join(lines)
