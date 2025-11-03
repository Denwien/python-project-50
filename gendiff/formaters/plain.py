def format_diff_plain(diff, path=""):
    lines = []

    def stringify(value):
        if isinstance(value, dict):
            return "[complex value]"
        if isinstance(value, str):
            return f"'{value}'"
        if value is None:
            return "null"
        return str(value).lower() if isinstance(value, bool) else str(value)

    for key, info in diff.items():
        property_path = f"{path}.{key}" if path else key
        status = info["status"]
        if status == "nested":
            lines.extend(format_diff_plain(info["children"], property_path))
        elif status == "added":
            lines.append(f"Property '{property_path}' was added with value: {stringify(info['value'])}")
        elif status == "removed":
            lines.append(f"Property '{property_path}' was removed")
        elif status == "updated":
            old = stringify(info["old_value"])
            new = stringify(info["new_value"])
            lines.append(f"Property '{property_path}' was updated. From {old} to {new}")
    return lines if path else "\n".join(lines)

    