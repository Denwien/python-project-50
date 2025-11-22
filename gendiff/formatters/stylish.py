INDENT = 2
SIGN_INDENT = 2


def _stringify(value, depth: int, extra_indent: int = 0) -> str:
    """
    Преобразует значение в строку с учётом вложенности без фигурных скобок.
    - dict -> блок со следующей строкой и дочерними ключами с увеличенным отступом
    - None -> 'null'
    - bool -> 'true'/'false'
    - иные типы -> str(value)
    """
    if isinstance(value, dict):
        lines = []
        indent = ' ' * ((depth + 1) * INDENT + extra_indent)
        for k, v in value.items():
            rendered = _stringify(v, depth + 1)
            if isinstance(v, dict):
                lines.append(f"{indent}{k}:{rendered}")
            else:
                lines.append(f"{indent}{k}: {rendered}")
        # Возвращаем с переводом строки, чтобы родитель мог поставить двоеточие
        return "\n" + "\n".join(lines)

    if value is None:
        return 'null'

    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def format_diff_stylish(diff, depth: int = 0) -> str:
    """Форматирование diff-дерева в стиль без фигурных скобок."""
    lines = []
    base_indent = ' ' * (depth * INDENT)

    for node in diff:
        key = node['name']
        action = node['action']

        if action == 'nested':
            lines.append(f"{base_indent}{key}:")
            lines.append(format_diff_stylish(node['children'], depth + 1))
            continue

        if action == 'unchanged':
            value = node['value']
            rendered = _stringify(value, depth)
            if isinstance(value, dict):
                lines.append(f"{base_indent}{key}:{rendered}")
            else:
                lines.append(f"{base_indent}{key}:{'' if rendered == '' else ' ' + rendered}")
            continue

        if action in ('added',):
            value = node['value']
            rendered = _stringify(value, depth)
            sign_indent = base_indent
            if isinstance(value, dict):
                lines.append(f"{sign_indent}+ {key}:{rendered}")
            else:
                lines.append(f"{sign_indent}+ {key}:{'' if rendered == '' else ' ' + rendered}")
            continue

        if action in ('removed', 'deleted'):
            value = node.get('old_value')
            rendered = _stringify(value, depth)
            sign_indent = base_indent
            if isinstance(value, dict):
                lines.append(f"{sign_indent}- {key}:{rendered}")
            else:
                lines.append(f"{sign_indent}- {key}:{'' if rendered == '' else ' ' + rendered}")
            continue

        if action in ('changed', 'modified'):
            old_value = node['old_value']
            new_value = node['new_value']
            old_rendered = _stringify(old_value, depth, SIGN_INDENT if isinstance(old_value, dict) else 0)
            new_rendered = _stringify(new_value, depth, SIGN_INDENT if isinstance(new_value, dict) else 0)
            sign_indent = base_indent
            if isinstance(old_value, dict):
                lines.append(f"{sign_indent}- {key}:{old_rendered}")
            else:
                lines.append(f"{sign_indent}- {key}:{'' if old_rendered == '' else ' ' + old_rendered}")
            if isinstance(new_value, dict):
                lines.append(f"{sign_indent}+ {key}:{new_rendered}")
            else:
                lines.append(f"{sign_indent}+ {key}:{'' if new_rendered == '' else ' ' + new_rendered}")
            continue

        raise ValueError(f"Unknown action in diff node: {action}")

    return "\n".join(lines)

