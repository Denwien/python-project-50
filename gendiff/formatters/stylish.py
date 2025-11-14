INDENT = 4
SIGN_ADDED = "+ "
SIGN_REMOVED = "- "
SIGN_NONE = "  "


def stringify(value, depth):
    if isinstance(value, dict):
        lines = ["{"]
        indent = " " * ((depth + 1) * INDENT)
        closing_indent = " " * (depth * INDENT)

        for key, inner in value.items():
            formatted = stringify(inner, depth + 1)
            lines.append(f"{indent}{SIGN_NONE}{key}: {formatted}")

        lines.append(f"{closing_indent}}}")
        return "\n".join(lines)

    if value is None:
        return "null"

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def make_stylish(diff, depth=0):
    lines = ["{"]
    indent = " " * (depth * INDENT)
    next_indent = " " * ((depth * INDENT) + INDENT)

    for node in diff:
        key = node["name"]
        action = node["action"]

        if action == "nested":
            children = make_stylish(node["children"], depth + 1)
            lines.append(f"{next_indent}{SIGN_NONE}{key}: {children}")
            continue

        if action == "unchanged":
            value = stringify(node["value"], depth + 1)
            lines.append(f"{next_indent}{SIGN_NONE}{key}: {value}")
            continue

        if action == "added":
            value = stringify(node["value"], depth + 1)
            lines.append(f"{next_indent}{SIGN_ADDED}{key}: {value}")
            continue

        if action == "deleted":
            value = stringify(node["old_value"], depth + 1)
            lines.append(f"{next_indent}{SIGN_REMOVED}{key}: {value}")
            continue

        if action == "modified":
            old = stringify(node["old_value"], depth + 1)
            new = stringify(node["new_value"], depth + 1)
            lines.append(f"{next_indent}{SIGN_REMOVED}{key}: {old}")
            lines.append(f"{next_indent}{SIGN_ADDED}{key}: {new}")
            continue

    lines.append(f"{indent}}}")
    return "\n".join(lines)


def format_diff_stylish(diff):
    return make_stylish(diff)
