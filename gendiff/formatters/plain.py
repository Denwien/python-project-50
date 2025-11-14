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


def walk_plain(node, path, lines):
    name = node.get("name")
    current_path = f"{path}.{name}" if path else name
    action = node.get("action")

    if action == "nested":
        for child in node["children"]:
            walk_plain(child, current_path, lines)
    elif action == "added":
        value = stringify(node["value"])
        lines.append(f"Property '{current_path}' was added with value: {value}")
    elif action == "deleted":
        lines.append(f"Property '{current_path}' was removed")
    elif action == "modified":
        old_val = stringify(node["old_value"])
        new_val = stringify(node["new_value"])
        msg = (
            f"Property '{current_path}' was updated. "
            f"From {old_val} to {new_val}"
        )
        lines.append(msg)


def format_plain(diff_tree):
    lines = []
    for node in diff_tree:
        walk_plain(node, "", lines)
    return "\n".join(lines)
