def format_value(value, depth):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if not isinstance(value, dict):
        return str(value)
    
    indent = "  " * depth
    lines = []
    for key, val in value.items():
        formatted_val = format_value(val, depth + 1)
        lines.append(f"{indent}{key}: {formatted_val}")
    return "\n" + "\n".join(lines)


def format_diff_stylish(diff, depth=0):
    lines = []
    base_indent = "  " * depth
    
    for node in diff:
        name = node["name"]
        action = node["action"]
        
        if action == "nested":
            lines.append(f"{base_indent}{name}:")
            nested_content = format_diff_stylish(node["children"], depth + 1)
            lines.append(nested_content)
        elif action == "unchanged":
            value = format_value(node["value"], depth + 2)
            if "\n" in str(value):
                lines.append(f"{base_indent}  {name}:{value}")
            else:
                lines.append(f"{base_indent}  {name}: {value}")
        elif action == "deleted":
            value = format_value(node["old_value"], depth + 2)
            if "\n" in str(value):
                lines.append(f"{base_indent}- {name}:{value}")
            else:
                lines.append(f"{base_indent}- {name}: {value}")
        elif action == "added":
            value = format_value(node["value"], depth + 2)
            if "\n" in str(value):
                lines.append(f"{base_indent}+ {name}:{value}")
            else:
                lines.append(f"{base_indent}+ {name}: {value}")
        elif action == "modified":
            old_value = format_value(node["old_value"], depth + 2)
            new_value = format_value(node["new_value"], depth + 2)
            if "\n" in str(old_value):
                lines.append(f"{base_indent}- {name}:{old_value}")
            else:
                lines.append(f"{base_indent}- {name}: {old_value}")
            if "\n" in str(new_value):
                lines.append(f"{base_indent}+ {name}:{new_value}")
            else:
                lines.append(f"{base_indent}+ {name}: {new_value}")
    
    return "\n".join(lines)


def format_stylish(diff)
    return format_diff_stylish(diff, depth=0)