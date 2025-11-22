INDENT = 4
SIGN_INDENT = 2  # оставим, даже если сейчас не используем — на логику не влияет
def format_diff_stylish(diff, depth: int = 0) -> str:
    """
    Форматирование АСТ различий в стиль stylish.
    """

    # В CLI-обёртке могут по ошибке передать уже ГОТОВУЮ строку diff.
    # В этом случае просто вернём её как есть.
    if isinstance(diff, str):
        return diff

    lines = ['{']
    base_indent = ' ' * (depth * INDENT)

    for node in diff:
        key = node['name']
        action = node['action']

        if action == 'nested':
            children_repr = format_diff_stylish(node['children'], depth + 1)
            lines.append(f"{base_indent}    {key}: {children_repr}")
            continue

        if action == 'unchanged':
            value_repr = _stringify(node['value'], depth + 1)
            lines.append(f"{base_indent}    {key}: {value_repr}")
            continue

        if action in ('added',):
            value_repr = _stringify(node['value'], depth + 1)
            lines.append(f"{base_indent}  + {key}: {value_repr}")
            continue

        if action in ('removed', 'deleted'):
            value_repr = _stringify(node['old_value'], depth + 1)
            lines.append(f"{base_indent}  - {key}: {value_repr}")
            continue

        if action in ('changed', 'modified'):
            old_repr = _stringify(node['old_value'], depth + 1)
            new_repr = _stringify(node['new_value'], depth + 1)
            lines.append(f"{base_indent}  - {key}: {old_repr}")
            lines.append(f"{base_indent}  + {key}: {new_repr}")
            continue

        raise ValueError(f"Unknown action in diff node: {action}")

    closing_indent = ' ' * (depth * INDENT)
    lines.append(f"{closing_indent}}}")
    return '\n'.join(lines)
