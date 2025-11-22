SEPARATOR = " "
ADD = '+ '
DEL = '- '
NONE = '  '


def format_value(value, spaces_count=2):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return str(value).lower()
    if isinstance(value, dict):
        indent = SEPARATOR * (spaces_count + 4)
        result_lines = []
        for key, inner_value in value.items():
            formatted_value = format_value(inner_value, spaces_count + 4)
            result_lines.append(f"{indent}{NONE}{key}: {formatted_value}")
        formatted_string = '\n'.join(result_lines)
        end_indent = SEPARATOR * (spaces_count + 2)
        return f"{{\n{formatted_string}\n{end_indent}}}"
    return f"{value}"


def _as_nodes_iter(diff):
    """Yield node-like dicts unified from either list-of-nodes or builder dict mapping."""
    if isinstance(diff, dict):
        # builder creates sorted keys already; keep order of insertion
        for key in diff.keys():
            item = diff[key]
            yield {
                'name': key,
                'action': item['action'],
                'value': item.get('value'),
                'old_value': item.get('old_value'),
                'new_value': item.get('new_value'),
                'children': item.get('children'),
            }
    else:
        for node in diff:
            yield node


def make_stylish_diff(diff, spaces_count=2):
    indent = SEPARATOR * spaces_count
    lines = []

    for item in _as_nodes_iter(diff):
        key = item['name']
        action = item['action']

        # Prefer correct field regardless of diff producer
        raw_value = item.get('value')
        raw_old_value = item.get('old_value')
        raw_new_value = item.get('new_value')

        value = format_value(raw_value, spaces_count)
        # For added nodes from builder, value is under 'value'
        new_value = format_value(raw_new_value if raw_new_value is not None else raw_value, spaces_count)
        # For deleted nodes from builder, old_value is under 'old_value', otherwise 'value'
        old_value = format_value(raw_old_value if raw_old_value is not None else raw_value, spaces_count)

        if action == "unchanged":
            lines.append(f"{indent}{NONE}{key}: {value}")
        elif action in ("modified", "changed"):
            lines.append(f"{indent}{DEL}{key}: {old_value}")
            lines.append(f"{indent}{ADD}{key}: {new_value}")
        elif action in ("deleted", "removed"):
            lines.append(f"{indent}{DEL}{key}: {old_value}")
        elif action in ("added",):
            lines.append(f"{indent}{ADD}{key}: {new_value}")
        elif action == 'nested':
            children = make_stylish_diff(item.get("children"), spaces_count + 4)
            lines.append(f"{indent}{NONE}{key}: {children}")
        else:
            raise ValueError(f"Unknown action: {action}")

    formatted_string = '\n'.join(lines)
    end_indent = SEPARATOR * (spaces_count - 2)

    return f"{{\n{formatted_string}\n{end_indent}}}"


def format_diff_stylish(data, depth: int = 0) -> str:
    return make_stylish_diff(data)

